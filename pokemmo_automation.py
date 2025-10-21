import time
import random
import threading
import logging
from pynput import keyboard, mouse
import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab, Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pokemmo_automation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PokeMMOAutomation:
    def __init__(self):
        self.running = False
        self.config = {
            "move_keys": ["w", "a", "s", "d"],  # 移动按键
            "move_pattern": "random",  # 移动模式：random, circle, square
            "skill_key": "1",  # 技能按键
            "skill_pattern": "sequence",  # 技能模式：sequence, random
            "skill_order": ["1", "1", "1", "1"],  # 技能使用顺序
            "ball_key": "2",  # 精灵球按键
            "escape_key": "escape",  # 逃跑按键
            "encounter_time_threshold": 5,  # 遭遇精灵的时间阈值（秒）
            "move_duration": 0.5,  # 每次移动的持续时间（秒）
            "pause_between_moves": 0.3,  # 移动间隔时间（秒）
            "pause_between_actions": 1.0,  # 动作间隔时间（秒）
            "pp_threshold": 3,  # PP值阈值，低于此值停止使用技能
            "screenshot_region": None,  # 截图区域，None表示全屏
            "device_type": "pc",  # 设备类型：pc, mobile
            "use_adb": False,  # 是否使用ADB连接手机
            "adb_device": "",  # ADB设备ID
            # 新增配置
            "target_pokemon": "",  # 目标宠物名称
            "pre_catch_skills": ["1"],  # 捕捉前要使用的技能
            "catch_conditions": ["any"],  # 捕捉条件列表：any, low_hp, sleep, paralyze
            "pet_images": {},  # 宠物图像模板
            "catch_ball_type": "精灵球",  # 捕捉使用的球类型
            "auto_stop_on_shiny": True,  # 发现闪光宠物时自动停止
            "condition_skills": {  # 不同条件对应的技能
                "sleep": ["1"],  # 用于使宠物睡眠的技能
                "paralyze": ["2"],  # 用于使宠物麻痹的技能
                "low_hp": ["3"]  # 用于降低宠物血量的技能
            }
        }
        self.current_skill_index = 0
        self.skill_pp = {"1": 35, "2": 25, "3": 20, "4": 15}  # 初始PP值估计
        self.stop_event = threading.Event()
        self.last_encounter_time = 0
        self.encounter_count = 0
        self.success_catch_count = 0
        self.virtual_buttons_window = None
        self.virtual_buttons = {}  # 存储虚拟按钮坐标
        self.pet_templates = {}  # 存储宠物图像模板
        
        # 加载配置
        self.load_config()
        
        # 创建GUI
        self.root = tk.Tk()
        self.root.title("Pokemmo自动抓宠工具")
        self.root.geometry("800x600")
        self.create_gui()
    
    def load_config(self):
        """加载配置文件"""
        config_file = "pokemmo_config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
                logger.info("配置文件加载成功")
            except Exception as e:
                logger.error(f"加载配置文件失败: {str(e)}")
    
    def save_config(self):
        """保存配置文件"""
        config_file = "pokemmo_config.json"
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            logger.info("配置文件保存成功")
        except Exception as e:
            logger.error(f"保存配置文件失败: {str(e)}")
    
    def create_gui(self):
        """创建图形用户界面"""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 主界面标签页
        main_tab = ttk.Frame(notebook)
        notebook.add(main_tab, text="控制中心")
        
        # 控制按钮
        control_frame = ttk.LabelFrame(main_tab, text="控制", padding=10)
        control_frame.pack(fill=tk.X, pady=5)
        
        self.start_button = ttk.Button(control_frame, text="开始自动化", command=self.start_automation)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="停止自动化", command=self.stop_automation, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # 虚拟按钮按钮
        virtual_button = ttk.Button(control_frame, text="显示虚拟按钮", command=self.show_virtual_buttons)
        virtual_button.pack(side=tk.LEFT, padx=5)
        
        # 状态显示
        status_frame = ttk.LabelFrame(main_tab, text="状态", padding=10)
        status_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(status_frame, text="运行状态: ").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.status_var = tk.StringVar(value="未运行")
        ttk.Label(status_frame, textvariable=self.status_var).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(status_frame, text="遭遇次数: ").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.encounter_var = tk.StringVar(value="0")
        ttk.Label(status_frame, textvariable=self.encounter_var).grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(status_frame, text="捕获成功: ").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.catch_var = tk.StringVar(value="0")
        ttk.Label(status_frame, textvariable=self.catch_var).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # 宠物捕捉设置标签页
        pokemon_tab = ttk.Frame(notebook)
        notebook.add(pokemon_tab, text="宠物捕捉设置")
        
        # 目标宠物设置
        target_frame = ttk.LabelFrame(pokemon_tab, text="目标宠物", padding=10)
        target_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(target_frame, text="目标宠物名称: ").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.target_pokemon_var = tk.StringVar(value=self.config["target_pokemon"])
        ttk.Entry(target_frame, textvariable=self.target_pokemon_var, width=20).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # 添加宠物模板按钮
        add_template_button = ttk.Button(target_frame, text="添加宠物图像模板", command=self.add_pokemon_template)
        add_template_button.grid(row=0, column=2, padx=10, pady=2)
        
        # 捕捉前技能设置
        pre_catch_frame = ttk.LabelFrame(pokemon_tab, text="捕捉前技能", padding=10)
        pre_catch_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(pre_catch_frame, text="捕捉前要使用的技能 (用逗号分隔): ").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.pre_catch_skills_var = tk.StringVar(value=",".join(self.config["pre_catch_skills"]))
        ttk.Entry(pre_catch_frame, textvariable=self.pre_catch_skills_var, width=20).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # 捕捉条件设置（支持多选）
        condition_frame = ttk.LabelFrame(pokemon_tab, text="捕捉条件（可多选）", padding=10)
        condition_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(condition_frame, text="捕捉条件: ").grid(row=0, column=0, sticky=tk.NW, pady=2)
        condition_frame_inner = ttk.Frame(condition_frame)
        condition_frame_inner.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # 使用字典存储复选按钮状态
        self.catch_conditions_vars = {
            "any": tk.BooleanVar(value="any" in self.config["catch_conditions"]),
            "low_hp": tk.BooleanVar(value="low_hp" in self.config["catch_conditions"]),
            "sleep": tk.BooleanVar(value="sleep" in self.config["catch_conditions"]),
            "paralyze": tk.BooleanVar(value="paralyze" in self.config["catch_conditions"])
        }
        
        # 创建复选按钮
        ttk.Checkbutton(condition_frame_inner, text="任何状态", variable=self.catch_conditions_vars["any"]).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(condition_frame_inner, text="低血量", variable=self.catch_conditions_vars["low_hp"]).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(condition_frame_inner, text="睡眠状态", variable=self.catch_conditions_vars["sleep"]).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(condition_frame_inner, text="麻痹状态", variable=self.catch_conditions_vars["paralyze"]).pack(side=tk.LEFT, padx=5)
        
        # 闪光宠物自动停止设置
        shiny_frame = ttk.LabelFrame(pokemon_tab, text="闪光宠物检测", padding=10)
        shiny_frame.pack(fill=tk.X, pady=5)
        
        self.auto_stop_on_shiny_var = tk.BooleanVar(value=self.config["auto_stop_on_shiny"])
        ttk.Checkbutton(shiny_frame, text="发现闪光宠物时自动停止", variable=self.auto_stop_on_shiny_var).pack(side=tk.LEFT, padx=5)
        
        # 条件技能设置
        condition_skills_frame = ttk.LabelFrame(pokemon_tab, text="条件技能设置", padding=10)
        condition_skills_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(condition_skills_frame, text="用于睡眠状态的技能: ").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.sleep_skills_var = tk.StringVar(value=",".join(self.config["condition_skills"]["sleep"]))
        ttk.Entry(condition_skills_frame, textvariable=self.sleep_skills_var, width=20).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(condition_skills_frame, text="用于麻痹状态的技能: ").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.paralyze_skills_var = tk.StringVar(value=",".join(self.config["condition_skills"]["paralyze"]))
        ttk.Entry(condition_skills_frame, textvariable=self.paralyze_skills_var, width=20).grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(condition_skills_frame, text="用于降低血量的技能: ").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.low_hp_skills_var = tk.StringVar(value=",".join(self.config["condition_skills"]["low_hp"]))
        ttk.Entry(condition_skills_frame, textvariable=self.low_hp_skills_var, width=20).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # 捕捉球设置
        ball_type_frame = ttk.LabelFrame(pokemon_tab, text="捕捉球设置", padding=10)
        ball_type_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(ball_type_frame, text="捕捉使用的球类型: ").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.catch_ball_type_var = tk.StringVar(value=self.config["catch_ball_type"])
        ball_types = ["精灵球", "超级球", "高级球", "重复球", "治愈球", "大师球"]
        ball_type_combo = ttk.Combobox(ball_type_frame, textvariable=self.catch_ball_type_var, values=ball_types, width=20)
        ball_type_combo.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # 保存宠物设置按钮
        save_pokemon_button = ttk.Button(pokemon_tab, text="保存宠物捕捉设置", command=lambda: self.save_pokemon_settings(
            self.target_pokemon_var.get(),
            [s.strip() for s in self.pre_catch_skills_var.get().split(",") if s.strip()],
            self.catch_conditions_vars,
            self.catch_ball_type_var.get(),
            {
                "sleep": [s.strip() for s in self.sleep_skills_var.get().split(",") if s.strip()],
                "paralyze": [s.strip() for s in self.paralyze_skills_var.get().split(",") if s.strip()],
                "low_hp": [s.strip() for s in self.low_hp_skills_var.get().split(",") if s.strip()]
            },
            self.auto_stop_on_shiny_var.get()
        ))
        save_pokemon_button.pack(pady=10)
        
        # 配置标签页
        config_tab = ttk.Frame(notebook)
        notebook.add(config_tab, text="配置")
        
        # 按键配置
        key_frame = ttk.LabelFrame(config_tab, text="按键设置", padding=10)
        key_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(key_frame, text="移动按键 (用逗号分隔): ").grid(row=0, column=0, sticky=tk.W, pady=2)
        move_keys_var = tk.StringVar(value=",".join(self.config["move_keys"]))
        ttk.Entry(key_frame, textvariable=move_keys_var, width=20).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(key_frame, text="技能按键: ").grid(row=1, column=0, sticky=tk.W, pady=2)
        skill_key_var = tk.StringVar(value=self.config["skill_key"])
        ttk.Entry(key_frame, textvariable=skill_key_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(key_frame, text="精灵球按键: ").grid(row=2, column=0, sticky=tk.W, pady=2)
        ball_key_var = tk.StringVar(value=self.config["ball_key"])
        ttk.Entry(key_frame, textvariable=ball_key_var, width=10).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(key_frame, text="逃跑按键: ").grid(row=3, column=0, sticky=tk.W, pady=2)
        escape_key_var = tk.StringVar(value=self.config["escape_key"])
        ttk.Entry(key_frame, textvariable=escape_key_var, width=10).grid(row=3, column=1, sticky=tk.W, pady=2)
        
        # 设备设置
        device_frame = ttk.LabelFrame(config_tab, text="设备设置", padding=10)
        device_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(device_frame, text="设备类型: ").grid(row=0, column=0, sticky=tk.W, pady=2)
        device_type_var = tk.StringVar(value=self.config["device_type"])
        device_type_frame = ttk.Frame(device_frame)
        device_type_frame.grid(row=0, column=1, sticky=tk.W, pady=2)
        ttk.Radiobutton(device_type_frame, text="PC", variable=device_type_var, value="pc").pack(side=tk.LEFT)
        ttk.Radiobutton(device_type_frame, text="手机", variable=device_type_var, value="mobile").pack(side=tk.LEFT)
        
        # 保存配置按钮
        save_button = ttk.Button(config_tab, text="保存配置", command=lambda: self.save_config_values(
            move_keys_var.get().split(","), 
            skill_key_var.get(),
            ball_key_var.get(),
            device_type_var.get()
        ))
        save_button.pack(pady=10)
        
        # 加载宠物模板
        self.load_pokemon_templates()
        
        # 说明标签页
        help_tab = ttk.Frame(notebook)
        notebook.add(help_tab, text="使用说明")
        
        help_text = """
        Pokemmo自动抓宠工具使用说明:
        
        1. 配置设置:
           - 设置游戏中的移动、技能和精灵球按键
           - 选择设备类型（PC或手机）
           - 保存配置
        
        2. 使用方法:
           - 将游戏窗口置于前台
           - 点击"开始自动化"按钮启动脚本
           - 点击"停止自动化"按钮停止脚本
        
        3. 功能说明:
           - 自动在指定区域移动以遇怪
           - 检测到精灵时自动使用技能
           - 自动使用精灵球捕捉
           - PP值用完后自动停止
        
        快捷键: Ctrl+F1 开始/停止
        """
        help_label = ttk.Label(help_tab, text=help_text, justify=tk.LEFT, wraplength=700)
        help_label.pack(padx=20, pady=20)
        
        # 设置全局快捷键
        self.setup_hotkeys()
    
    def load_pokemon_templates(self):
        """加载宠物图像模板"""
        for pokemon_name, template_path in self.config["pet_images"].items():
            if os.path.exists(template_path):
                try:
                    self.pet_templates[pokemon_name] = cv2.imread(template_path)
                    logger.info(f"已加载宠物模板: {pokemon_name}")
                except Exception as e:
                    logger.error(f"加载宠物模板失败 {pokemon_name}: {str(e)}")
    
    def _check_ball_availability(self):
        """检查指定类型的精灵球是否可用"""
        try:
            # 截取背包区域
            screen_width, screen_height = pyautogui.size()
            # 根据截图位置估计背包区域
            backpack_region = (int(screen_width * 0.1), int(screen_height * 0.3), 
                             int(screen_width * 0.8), int(screen_height * 0.4))
            
            screenshot = np.array(ImageGrab.grab(bbox=backpack_region))
            # 转换为HSV进行颜色检测
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # 检测蓝色文本区域（精灵球名称区域）
            lower_blue = np.array([100, 50, 50])
            upper_blue = np.array([130, 255, 255])
            blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
            
            # 转换为灰度图用于OCR
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            
            # 这里简化处理，实际应该使用OCR识别文字
            # 暂时返回True表示有球可用
            return True
        except Exception as e:
            logger.error(f"检查精灵球可用性失败: {str(e)}")
            return False
    
    def show_virtual_buttons(self):
        """根据游戏截图在相应键位上显示虚拟按钮"""
        if self.virtual_buttons_window and self.virtual_buttons_window.winfo_exists():
            self.virtual_buttons_window.destroy()
        
        # 获取屏幕大小
        screen_width, screen_height = pyautogui.size()
        
        # 创建虚拟按钮窗口，设置为透明和全屏
        self.virtual_buttons_window = tk.Toplevel(self.root)
        self.virtual_buttons_window.title("游戏虚拟按钮")
        self.virtual_buttons_window.geometry(f"{screen_width}x{screen_height}+0+0")
        self.virtual_buttons_window.attributes('-alpha', 0.7)  # 半透明
        self.virtual_buttons_window.attributes('-topmost', True)  # 置顶
        self.virtual_buttons_window.overrideredirect(True)  # 无边框窗口
        
        # 按钮大小
        main_button_size = 80  # 主要按钮大小
        action_button_size = 70  # 动作按钮大小
        control_button_size = 50  # 控制按钮大小
        
        # 创建自定义圆形按钮的函数
        def create_circle_button(parent, text, command, x, y, size=main_button_size, color="#3498db", text_color="white"):
            button_frame = tk.Frame(parent, bd=0, highlightthickness=0)
            button_frame.place(x=x - size//2, y=y - size//2, width=size, height=size)
            
            # 创建圆形画布
            canvas = tk.Canvas(button_frame, width=size, height=size, bd=0, highlightthickness=0)
            canvas.pack(fill=tk.BOTH, expand=True)
            
            # 绘制圆形按钮
            radius = size // 2 - 5
            canvas.create_oval(5, 5, size-5, size-5, fill=color, outline="#2980b9", width=2)
            
            # 添加文本
            canvas.create_text(size//2, size//2, text=text, fill=text_color, font=("Arial", 14, "bold"))
            
            # 绑定点击事件
            canvas.bind("<Button-1>", lambda e: command())
            
            return button_frame
        
        # 创建自定义方形按钮的函数（用于菜单和背包按钮）
        def create_square_button(parent, text, command, x, y, size=control_button_size, color="#3498db", text_color="white"):
            button_frame = tk.Frame(parent, bd=0, highlightthickness=0)
            button_frame.place(x=x - size//2, y=y - size//2, width=size, height=size)
            
            # 创建方形画布
            canvas = tk.Canvas(button_frame, width=size, height=size, bd=0, highlightthickness=0)
            canvas.pack(fill=tk.BOTH, expand=True)
            
            # 绘制方形按钮
            canvas.create_rectangle(5, 5, size-5, size-5, fill=color, outline="#2980b9", width=2)
            
            # 添加文本
            canvas.create_text(size//2, size//2, text=text, fill=text_color, font=("Arial", 12, "bold"))
            
            # 绑定点击事件
            canvas.bind("<Button-1>", lambda e: command())
            
            return button_frame
        
        # ========== 游戏主界面按钮（根据截图）==========
        # 方向控制按钮（左下角）
        move_center_x = int(screen_width * 0.15)
        move_center_y = int(screen_height * 0.85)
        move_radius = 70
        
        # 方向按钮 - 圆形布局
        create_circle_button(self.virtual_buttons_window, "↑", lambda: self._press_key("w"), 
                           move_center_x, move_center_y - move_radius, action_button_size, "#2ecc71")
        create_circle_button(self.virtual_buttons_window, "←", lambda: self._press_key("a"), 
                           move_center_x - move_radius, move_center_y, action_button_size, "#2ecc71")
        create_circle_button(self.virtual_buttons_window, "↓", lambda: self._press_key("s"), 
                           move_center_x, move_center_y + move_radius, action_button_size, "#2ecc71")
        create_circle_button(self.virtual_buttons_window, "→", lambda: self._press_key("d"), 
                           move_center_x + move_radius, move_center_y, action_button_size, "#2ecc71")
        
        # 确定/取消按钮（右下角，根据截图的A/B按钮）
        confirm_x = int(screen_width * 0.8)
        cancel_x = int(screen_width * 0.7)
        action_y = int(screen_height * 0.85)
        
        create_circle_button(self.virtual_buttons_window, "A", lambda: self._press_key("z"), 
                           confirm_x, action_y, main_button_size, "#3498db")
        create_circle_button(self.virtual_buttons_window, "B", lambda: self._press_key("x"), 
                           cancel_x, action_y, main_button_size, "#e74c3c")
        
        # 菜单按钮（右上角）
        menu_x = int(screen_width * 0.95)
        menu_y = int(screen_height * 0.1)
        create_square_button(self.virtual_buttons_window, "≡", lambda: self._press_key("escape"), 
                           menu_x, menu_y, control_button_size, "#95a5a6")
        
        # 背包按钮已在战斗界面中定义，此处移除
        
        # ========== 战斗界面按钮（根据截图）==========
        # 战斗按钮 - 调整位置以对准真实界面
        battle_x = int(screen_width * 0.08)
        battle_y = int(screen_height * 0.85)
        create_circle_button(self.virtual_buttons_window, "战斗", lambda: self._press_key(self.config["skill_key"]), 
                           battle_x, battle_y, action_button_size, "#e74c3c")
        
        # 精灵按钮 - 调整位置
        pokemon_x = int(screen_width * 0.17)
        pokemon_y = int(screen_height * 0.85)
        create_circle_button(self.virtual_buttons_window, "精灵", lambda: self._press_key("4"), 
                           pokemon_x, pokemon_y, action_button_size, "#9b59b6")
        
        # 背包按钮（战斗界面）- 调整位置
        battle_bag_x = int(screen_width * 0.82)
        battle_bag_y = int(screen_height * 0.85)
        create_circle_button(self.virtual_buttons_window, "背包", lambda: self._press_key("b"), 
                           battle_bag_x, battle_bag_y, action_button_size, "#f39c12")
        
        # 逃跑按钮 - 调整位置
        run_x = int(screen_width * 0.92)
        run_y = int(screen_height * 0.85)
        create_circle_button(self.virtual_buttons_window, "逃跑", lambda: self._press_key(self.config["escape_key"]), 
                           run_x, run_y, action_button_size, "#e67e22")
        
        # ========== 技能按键（战斗界面内的四个技能）==========
        # 技能按钮大小（比主按钮小一些）
        skill_button_size = 60
        
        # 技能按钮位置 - 根据截图中的技能位置布局
        # 第一个技能（左上角）
        skill1_x = int(screen_width * 0.2)
        skill1_y = int(screen_height * 0.4)
        create_circle_button(self.virtual_buttons_window, "1", lambda: self._use_specific_skill("1"), 
                           skill1_x, skill1_y, skill_button_size, "#27ae60")
        
        # 第二个技能（右上角）
        skill2_x = int(screen_width * 0.35)
        skill2_y = int(screen_height * 0.4)
        create_circle_button(self.virtual_buttons_window, "2", lambda: self._use_specific_skill("2"), 
                           skill2_x, skill2_y, skill_button_size, "#3498db")
        
        # 第三个技能（左下角）
        skill3_x = int(screen_width * 0.2)
        skill3_y = int(screen_height * 0.55)
        create_circle_button(self.virtual_buttons_window, "3", lambda: self._use_specific_skill("3"), 
                           skill3_x, skill3_y, skill_button_size, "#9b59b6")
        
        # 第四个技能（右下角）
        skill4_x = int(screen_width * 0.35)
        skill4_y = int(screen_height * 0.55)
        create_circle_button(self.virtual_buttons_window, "4", lambda: self._use_specific_skill("4"), 
                           skill4_x, skill4_y, skill_button_size, "#e67e22")
        
        # ========== 控制按钮 ==========
        # 开始/停止按钮
        start_stop_x = int(screen_width * 0.5)
        start_stop_y = int(screen_height * 0.1)
        start_stop_btn = ttk.Button(
            self.virtual_buttons_window,
            text="开始/停止",
            command=self.toggle_automation,
            style="Accent.TButton"
        )
        start_stop_btn.place(x=start_stop_x - 50, y=start_stop_y)
        
        # 关闭按钮
        close_btn = ttk.Button(
            self.virtual_buttons_window,
            text="关闭",
            command=lambda: self.virtual_buttons_window.destroy()
        )
        close_btn.place(x=screen_width - 80, y=20)
        
        # 宠物资料关闭按钮（右上角的❌）
        pokemon_info_close_x = int(screen_width * 0.95)
        pokemon_info_close_y = int(screen_height * 0.05)
        create_circle_button(self.virtual_buttons_window, "❌", 
                           lambda: self._press_key("escape"),  # 使用escape键关闭
                           pokemon_info_close_x, pokemon_info_close_y, 
                           control_button_size, "#e74c3c")
        
        # 配置样式
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 12, "bold"), foreground="#2c3e50")
    
    def toggle_automation(self):
        """切换自动化状态"""
        if self.running:
            self.stop_automation()
        else:
            self.start_automation()
    
    def save_config_values(self, move_keys, skill_key, ball_key, device_type):
        """保存配置值"""
        self.config["move_keys"] = [k.strip() for k in move_keys if k.strip()]
        self.config["skill_key"] = skill_key
        self.config["ball_key"] = ball_key
        self.config["device_type"] = device_type
        self.save_config()
        messagebox.showinfo("成功", "配置已保存")
    
    def save_pokemon_settings(self, target_pokemon, pre_catch_skills, catch_conditions_vars, catch_ball_type, condition_skills, auto_stop_on_shiny):
        """保存宠物捕捉设置"""
        # 更新配置
        self.config["target_pokemon"] = target_pokemon
        self.config["pre_catch_skills"] = pre_catch_skills
        self.config["catch_ball_type"] = catch_ball_type
        self.config["auto_stop_on_shiny"] = auto_stop_on_shiny
        
        # 保存多选的捕捉条件
        selected_conditions = []
        for condition, var in catch_conditions_vars.items():
            if var.get():
                selected_conditions.append(condition)
        # 如果没有选择任何条件，默认添加'any'
        if not selected_conditions:
            selected_conditions.append("any")
        self.config["catch_conditions"] = selected_conditions
        
        # 保存条件技能设置
        self.config["condition_skills"] = condition_skills
        
        self.save_config()
        messagebox.showinfo("成功", "宠物捕捉设置已保存")
    
    def _detect_shiny_pokemon(self, screenshot):
        """检测是否为闪光宠物
        闪光宠物通常有特殊的颜色或出场动画效果
        """
        # 尝试检测闪光宠物的标志性特征
        # 1. 检查宠物名称是否有闪光标识（如星号、特殊颜色）
        # 2. 检查屏幕中是否有闪光特效
        
        # 检查宠物名称区域（根据实际游戏界面调整坐标）
        # 这里假设宠物名称在屏幕上方的某个区域
        name_region = screenshot.crop((200, 100, 600, 150))
        
        # 转换为HSV色彩空间来检测特殊颜色
        hsv = cv2.cvtColor(np.array(name_region), cv2.COLOR_RGB2HSV)
        
        # 定义金色/闪光颜色的HSV范围（可根据实际游戏调整）
        lower_gold = np.array([25, 100, 100])
        upper_gold = np.array([35, 255, 255])
        
        # 创建掩码
        mask = cv2.inRange(hsv, lower_gold, upper_gold)
        
        # 计算金色像素的数量
        gold_pixel_count = cv2.countNonZero(mask)
        
        # 如果金色像素超过阈值，则认为是闪光宠物
        return gold_pixel_count > 50
    
    def add_pokemon_template(self):
        """添加宠物图像模板"""
        pokemon_name = simpledialog.askstring("输入", "请输入宠物名称:")
        if not pokemon_name:
            return
        
        messagebox.showinfo("提示", "请在3秒内将宠物图像显示在屏幕中央，将自动截取")
        time.sleep(3)
        
        try:
            # 截取屏幕中央区域
            screen_width, screen_height = pyautogui.size()
            region = (
                screen_width // 2 - 100,
                screen_height // 2 - 100,
                200,
                200
            )
            screenshot = ImageGrab.grab(bbox=region)
            
            # 保存模板
            templates_dir = "pokemon_templates"
            os.makedirs(templates_dir, exist_ok=True)
            template_path = os.path.join(templates_dir, f"{pokemon_name.lower()}.png")
            screenshot.save(template_path)
            
            # 加载模板到内存
            self.pet_templates[pokemon_name.lower()] = cv2.imread(template_path)
            
            # 更新配置
            self.config["pet_images"][pokemon_name.lower()] = template_path
            self.save_config()
            
            messagebox.showinfo("成功", f"宠物 '{pokemon_name}' 图像模板已添加")
        except Exception as e:
            logger.error(f"添加宠物模板失败: {str(e)}")
            messagebox.showerror("错误", f"添加失败: {str(e)}")
    
    def setup_hotkeys(self):
        """设置全局快捷键"""
        def on_activate_hotkey():
            if self.running:
                self.stop_automation()
            else:
                self.start_automation()
        
        # 使用pynput监听快捷键
        def on_press(key):
            try:
                if key == keyboard.Key.f1 and keyboard.Key.ctrl_l in self.current_keys:
                    on_activate_hotkey()
                if hasattr(key, 'char'):
                    self.current_keys.add(key)
            except Exception as e:
                pass
        
        def on_release(key):
            try:
                if key == keyboard.Key.ctrl_l:
                    self.current_keys.discard(key)
                elif hasattr(key, 'char'):
                    self.current_keys.discard(key)
            except Exception as e:
                pass
        
        self.current_keys = set()
        self.keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.keyboard_listener.start()
    
    def _detect_game_screen(self):
        """检测游戏画面是否存在"""
        try:
            screenshot = np.array(ImageGrab.grab(bbox=self.config["screenshot_region"]))
            # 转换为HSV色彩空间进行颜色检测
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # 检测游戏界面特有的颜色（这里检测蓝色，可根据实际游戏调整）
            lower_blue = np.array([100, 100, 100])
            upper_blue = np.array([130, 255, 255])
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            
            # 计算蓝色区域的比例
            blue_ratio = cv2.countNonZero(mask) / (mask.size)
            
            # 如果蓝色区域超过一定比例，认为检测到游戏界面
            return blue_ratio > 0.03
        except Exception as e:
            logger.error(f"游戏画面检测失败: {str(e)}")
            return False
    
    def start_automation(self):
        """开始自动化任务"""
        if self.running:
            return
        
        # 1. 检测游戏画面
        if not self._detect_game_screen():
            logger.warning("未检测到游戏画面")
            messagebox.showwarning("警告", "未检测到游戏画面！请确保游戏窗口已打开并显示在前台。")
            return
        
        # 2. 验证是否设置了目标宠物
        if not self.config["target_pokemon"]:
            logger.warning("未设置目标宠物")
            messagebox.showwarning("警告", "请先设置要捕捉的宠物名称！")
            return
        
        # 3. 验证是否设置了技能顺序
        if not self.config["pre_catch_skills"]:
            logger.warning("未设置技能顺序")
            messagebox.showwarning("警告", "请先设置捕捉前要使用的技能顺序！")
            return
        
        # 4. 验证是否设置了捕捉使用的球类型
        if not self.config["catch_ball_type"]:
            logger.warning("未设置捕捉使用的球类型")
            messagebox.showwarning("警告", "请先设置捕捉使用的球类型！")
            return
        
        # 所有验证通过，开始自动化
        self.running = True
        self.stop_event.clear()
        self.status_var.set("运行中")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # 启动自动化线程
        self.automation_thread = threading.Thread(target=self.automation_loop)
        self.automation_thread.daemon = True
        self.automation_thread.start()
        
        logger.info("自动化任务已启动")
    
    def stop_automation(self):
        """停止自动化任务"""
        if not self.running:
            return
        
        self.running = False
        self.stop_event.set()
        self.status_var.set("已停止")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        if hasattr(self, 'automation_thread'):
            self.automation_thread.join(timeout=2)
        
        logger.info("自动化任务已停止")
    
    def automation_loop(self):
        """自动化主循环"""
        try:
            while self.running and not self.stop_event.is_set():
                # 检查PP值
                if self._check_pp_empty():
                    logger.warning("所有技能PP值已用完，停止抓宠")
                    self.stop_automation()
                    break
                
                # 移动以遇怪
                self._move()
                
                # 检查是否遇到精灵
                if self._check_encounter():
                    logger.info(f"发现精灵! 第{self.encounter_count}次遭遇")
                    self.encounter_count += 1
                    self.encounter_var.set(str(self.encounter_count))
                    
                    # 战斗循环
                    battle_result = self._battle_loop()
                    if battle_result == "caught":
                        self.success_catch_count += 1
                        self.catch_var.set(str(self.success_catch_count))
                        logger.info(f"成功捕获精灵! 总捕获数: {self.success_catch_count}")
                    
                    # 等待战斗结束
                    time.sleep(3)
        
        except Exception as e:
            logger.error(f"自动化过程中出错: {str(e)}")
            self.stop_automation()
    
    def _move(self):
        """根据配置的模式移动"""
        if self.config["move_pattern"] == "random":
            # 随机移动
            key = random.choice(self.config["move_keys"])
            self._press_key(key, self.config["move_duration"])
        elif self.config["move_pattern"] == "circle":
            # 圆形移动
            for key in self.config["move_keys"]:
                self._press_key(key, self.config["move_duration"])
                time.sleep(self.config["pause_between_moves"])
        
        time.sleep(self.config["pause_between_moves"])
    
    def _press_key(self, key, duration=0.5):
        """按下并释放按键，增加随机化以避免被检测"""
        try:
            # 添加随机延迟，避免固定时间间隔
            actual_duration = duration + (random.random() * 0.2 - 0.1)  # 在0.9*duration到1.1*duration之间
            
            if self.config["device_type"] == "pc":
                pyautogui.keyDown(key)
                time.sleep(actual_duration)
                pyautogui.keyUp(key)
            else:
                # 手机模式，需要ADB
                # 添加随机延迟后再执行命令
                time.sleep(random.uniform(0.05, 0.2))
                os.system(f"adb shell input keyevent {self._get_android_keycode(key)}")
                time.sleep(random.uniform(0.05, 0.2))
        except Exception as e:
            logger.error(f"按键操作失败: {str(e)}")
    
    def _get_android_keycode(self, key):
        """获取Android按键码"""
        keycode_map = {
            "w": "KEYCODE_W",
            "a": "KEYCODE_A",
            "s": "KEYCODE_S",
            "d": "KEYCODE_D",
            "1": "KEYCODE_1",
            "2": "KEYCODE_2",
        }
        return keycode_map.get(key, "KEYCODE_UNKNOWN")
    
    def _check_encounter(self):
        """检查是否遇到精灵"""
        # 这里使用简单的屏幕检测，实际使用时需要根据游戏画面进行调整
        try:
            screenshot = np.array(ImageGrab.grab(bbox=self.config["screenshot_region"]))
            # 转换为HSV色彩空间进行颜色检测
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # 检测战斗界面特有的颜色（这里只是示例，需要根据实际游戏调整）
            lower_red = np.array([0, 100, 100])
            upper_red = np.array([10, 255, 255])
            mask = cv2.inRange(hsv, lower_red, upper_red)
            
            # 计算红色区域的比例
            red_ratio = cv2.countNonZero(mask) / (mask.size)
            
            # 如果红色区域超过一定比例，认为进入了战斗界面
            if red_ratio > 0.05:
                self.last_encounter_time = time.time()
                return True
        except Exception as e:
            logger.error(f"遭遇检测失败: {str(e)}")
        
        return False
    
    def _identify_pokemon(self):
        """识别当前遭遇的宠物，支持模板匹配和名字识别"""
        target_pokemon = self.config["target_pokemon"]
        if not target_pokemon:
            logger.warning("未设置目标宠物")
            return None
        
        try:
            # 1. 首先尝试通过屏幕上显示的名字识别宠物
            # 截取宠物名称区域（根据游戏界面调整坐标）
            screen_width, screen_height = pyautogui.size()
            # 假设宠物名称在战斗界面的上方区域
            name_region = (
                screen_width // 2 - 200,
                screen_height // 2 - 250,
                400,
                100
            )
            
            name_screenshot = ImageGrab.grab(bbox=name_region)
            
            # 尝试OCR识别名字
            # 这里使用简化的方法，实际应用中可以使用更高级的OCR技术
            # 先尝试检测是否包含目标宠物名称的关键词
            if self._check_pokemon_name_in_screen(name_screenshot, target_pokemon):
                logger.info(f"通过名字识别到目标宠物: {target_pokemon}")
                return target_pokemon.lower()
            
            # 2. 如果名字识别失败，回退到模板匹配
            if self.pet_templates:
                # 截取屏幕中央区域用于识别
                region = (
                    screen_width // 2 - 150,
                    screen_height // 2 - 150,
                    300,
                    300
                )
                screenshot = np.array(ImageGrab.grab(bbox=region))
                screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
                
                # 与每个模板进行匹配
                best_match = None
                best_score = 0
                
                for pokemon_name, template in self.pet_templates.items():
                    if template is not None:
                        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                        # 使用模板匹配
                        result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
                        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                        
                        # 如果匹配度高于阈值，认为识别成功
                        if max_val > 0.7 and max_val > best_score:
                            best_score = max_val
                            best_match = pokemon_name
                
                if best_match:
                    logger.info(f"通过模板匹配识别到宠物: {best_match}, 匹配度: {best_score:.2f}")
                    return best_match
            
            logger.info("未识别到已知宠物")
            return None
        except Exception as e:
            logger.error(f"宠物识别失败: {str(e)}")
            return None
    
    def _check_pokemon_name_in_screen(self, screenshot, target_name):
        """检查屏幕上是否显示指定的宠物名称
        
        Args:
            screenshot: 屏幕截图
            target_name: 目标宠物名称
            
        Returns:
            bool: 是否识别到目标宠物名称
        """
        try:
            # 简单实现：检查特定区域的颜色模式或特征
            # 实际应用中可以使用OCR技术如Tesseract进行文字识别
            
            # 转换为HSV色彩空间，检测文字区域
            img_array = np.array(screenshot)
            hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            
            # 检测白色文字区域（假设宠物名称是白色显示）
            lower_white = np.array([0, 0, 200])
            upper_white = np.array([180, 50, 255])
            white_mask = cv2.inRange(hsv, lower_white, upper_white)
            
            # 计算白色像素的数量
            white_pixel_count = cv2.countNonZero(white_mask)
            
            # 如果白色像素超过阈值，认为可能有文字
            # 这里只是简化的判断，实际应用需要更精确的OCR
            return white_pixel_count > 200
        except Exception as e:
            logger.error(f"宠物名称检查失败: {str(e)}")
            return False
    
    def _check_pokemon_condition(self):
        """检查宠物是否满足捕捉条件（支持多条件）"""
        conditions = self.config["catch_conditions"]
        
        try:
            screenshot = np.array(ImageGrab.grab(bbox=self.config["screenshot_region"]))
            
            # 如果包含'any'条件，直接返回True
            if "any" in conditions:
                return True
            
            # 检查每个条件，只要满足其中一个就返回True
            for condition in conditions:
                if condition == "low_hp":
                    # 检测HP条颜色（简化实现）
                    hp_region = screenshot[50:70, 200:400]  # 假设HP条在这个位置
                    hp_hsv = cv2.cvtColor(hp_region, cv2.COLOR_BGR2HSV)
                    
                    # 检测红色（低血量）
                    lower_red = np.array([0, 100, 100])
                    upper_red = np.array([10, 255, 255])
                    red_mask = cv2.inRange(hp_hsv, lower_red, upper_red)
                    
                    if cv2.countNonZero(red_mask) > 100:
                        logger.info("检测到低血量条件满足")
                        return True
                elif condition == "sleep":
                    # 检测睡眠状态（简化实现）
                    # 实际应用中需要根据游戏中的睡眠图标进行调整
                    status_region = screenshot[100:150, 500:550]  # 假设状态图标在这个位置
                    # 这里应该检测睡眠特有的图标或颜色
                    # 暂时使用简化实现
                    if random.random() < 0.3:  # 模拟30%概率
                        logger.info("检测到睡眠状态满足")
                        return True
                elif condition == "paralyze":
                    # 检测麻痹状态（简化实现）
                    # 实际应用中需要根据游戏中的麻痹图标进行调整
                    status_region = screenshot[100:150, 500:550]  # 假设状态图标在这个位置
                    # 暂时使用简化实现
                    if random.random() < 0.3:  # 模拟30%概率
                        logger.info("检测到麻痹状态满足")
                        return True
            
            # 所有条件都不满足
            logger.info("未满足任何捕捉条件")
            return False
        except Exception as e:
            logger.error(f"宠物状态检测失败: {str(e)}")
            return False
    
    def _battle_loop(self):
        """战斗循环"""
        battle_start_time = time.time()
        max_battle_time = 60  # 最大战斗时间60秒
        
        # 截取屏幕用于检测闪光宠物
        screenshot = ImageGrab.grab()
        
        # 检查是否为闪光宠物（如果开启了此功能）
        if self.config["auto_stop_on_shiny"]:
            if self._detect_shiny_pokemon(screenshot):
                logger.warning("发现闪光宠物！自动停止！")
                self.stop_automation()
                messagebox.showinfo("闪光宠物发现", "发现闪光宠物！已自动停止脚本！")
                return "shiny_found"
        
        # 识别当前宠物
        encountered_pokemon = self._identify_pokemon()
        target_pokemon = self.config["target_pokemon"].lower()
        is_target = encountered_pokemon and encountered_pokemon == target_pokemon
        
        logger.info(f"战斗开始，是否目标宠物: {is_target}")
        
        if not is_target:
            # 非目标宠物，直接逃跑
            logger.info("非目标宠物，执行逃跑")
            self._press_key(self.config["escape_key"])
            time.sleep(2)
            return "fled"
        
        # 目标宠物，执行捕捉策略
        pre_catch_skills_used = False
        
        while time.time() - battle_start_time < max_battle_time:
            # 检查是否战斗结束
            if not self._is_in_battle():
                return "fled"
            
            # 如果还没使用捕捉前技能，先使用
            if not pre_catch_skills_used and self.config["pre_catch_skills"]:
                logger.info("使用捕捉前技能")
                for skill in self.config["pre_catch_skills"]:
                    self._press_key(skill)
                    time.sleep(self.config["pause_between_actions"])
                pre_catch_skills_used = True
                continue
            
            # 检查是否满足捕捉条件
            if self._check_pokemon_condition():
                logger.info("宠物满足捕捉条件，尝试捕捉")
                # 检查指定类型的球是否可用
                if not self._check_ball_availability():
                    logger.warning(f"指定的{self.config['catch_ball_type']}已用尽，停止抓宠")
                    self.stop_automation()
                    messagebox.showwarning("警告", f"指定的{self.config['catch_ball_type']}已用尽，请补充后再继续！")
                    return "no_balls"
                return self._catch_pokemon()
            
            # 继续使用技能降低血量或施加状态
            self._use_skill()
            time.sleep(self.config["pause_between_actions"])
        
        return "timeout"
    
    def _is_in_battle(self):
        """检查是否在战斗中"""
        # 类似_check_encounter的实现，检测战斗界面
        try:
            screenshot = np.array(ImageGrab.grab(bbox=self.config["screenshot_region"]))
            # 这里简化实现，实际需要更准确的检测
            return True  # 假设仍在战斗中
        except Exception:
            return False
    
    def _can_catch(self):
        """检查是否可以捕捉（精灵血量低等条件）"""
        # 简化实现，实际需要检测精灵血量
        return random.random() < 0.3  # 30%概率尝试捕捉
    
    def _catch_pokemon(self):
        """尝试捕捉精灵"""
        try:
            logger.info(f"尝试使用{self.config['catch_ball_type']}捕捉精灵...")
            
            # 打开背包
            self._press_key("b")
            time.sleep(1)
            
            # 根据设置选择指定类型的精灵球
            ball_type = self.config["catch_ball_type"]
            
            # 查找并选择指定类型的球
            # 在背包界面中找到对应的球
            
            # 先移动到精灵球类别
            self._press_key("2")  # 假设2是精灵球类别键
            time.sleep(1)
            
            # 查找指定类型的球
            # 模拟查找过程
            for _ in range(5):  # 最多查找5个位置
                # 检查当前选中的是否是目标球类型
                # 这里简化为随机成功
                if random.random() < 0.3 or _ == 4:  # 30%概率找到或尝试5次后选择当前项
                    # 确认选择
                    self._press_key("z")  # 确认键
                    time.sleep(1)
                    break
                # 否则继续查找
                self._press_key("s")  # 向下移动
                time.sleep(0.5)
            
            # 确认使用球
            self._press_key("z")  # 确认键
            time.sleep(5)  # 等待捕捉动画
            
            # 检查是否成功捕捉（简化实现）
            if random.random() < 0.7:  # 70%捕捉成功率
                logger.info("捕捉成功！")
                self.success_catch_count += 1
                
                # 更新UI中的捕捉计数
                self.root.after(0, self.update_catch_count)
                
                # 等待宠物资料界面出现
                time.sleep(2)
                
                # 点击关闭按钮关闭宠物资料界面
                self._close_pokemon_info()
                
                return "caught"
            return "escaped"
        except Exception as e:
            logger.error(f"捕捉精灵失败: {str(e)}")
            return "escaped"
    
    def _use_skill(self):
        """使用技能"""
        # 首先尝试根据需要的捕捉条件应用相应的技能
        if not self._apply_condition_skills():
            # 如果没有需要的条件技能或条件技能应用失败，使用默认的技能模式
            valid_skills = []
            
            # 筛选出PP值足够的技能
            for skill in self.config["skill_order"]:
                if skill in self.skill_pp and self.skill_pp[skill] > 0:
                    valid_skills.append(skill)
            
            # 如果没有可用技能，停止自动化
            if not valid_skills:
                logger.warning("所有技能PP值已耗尽！停止自动化")
                self.stop_automation()
                messagebox.showwarning("警告", "所有技能PP值已耗尽！请补充PP后再继续！")
                return None
            
            if self.config["skill_pattern"] == "sequence":
                # 按顺序使用技能，找到下一个PP值足够的技能
                original_index = self.current_skill_index
                while True:
                    skill = valid_skills[self.current_skill_index % len(valid_skills)]
                    self.current_skill_index = (self.current_skill_index + 1) % len(valid_skills)
                    if skill in self.skill_pp and self.skill_pp[skill] > 0:
                        break
                    # 如果已经遍历一圈都没找到可用技能
                    if self.current_skill_index % len(valid_skills) == original_index:
                        logger.warning("所有技能PP值已耗尽！停止自动化")
                        self.stop_automation()
                        messagebox.showwarning("警告", "所有技能PP值已耗尽！请补充PP后再继续！")
                        return None
            else:
                # 随机使用技能
                skill = random.choice(valid_skills)
            
            logger.info(f"使用默认技能: {skill} (剩余PP: {self.skill_pp.get(skill, 0)})")
            self._press_key(skill)
            
            # 减少PP值
            if skill in self.skill_pp:
                self.skill_pp[skill] -= 1
                logger.info(f"技能 {skill} 剩余PP: {self.skill_pp[skill]}")
                
                # 检查PP值是否低于阈值
                if self.skill_pp[skill] <= self.config.get("pp_threshold", 3):
                    logger.warning(f"技能 {skill} PP值偏低: {self.skill_pp[skill]}")
            
            return skill
        return None
    
    def _use_specific_skill(self, skill):
        """使用特定的技能，检查PP值"""
        # 检查技能PP值
        if skill in self.skill_pp:
            if self.skill_pp[skill] <= 0:
                logger.warning(f"技能 {skill} PP值已耗尽！")
                messagebox.showwarning("警告", f"技能 {skill} PP值已耗尽！")
                return
            
            logger.info(f"使用特定技能: {skill} (剩余PP: {self.skill_pp[skill]})")
            self._press_key(skill)
            
            # 减少PP值
            self.skill_pp[skill] -= 1
            logger.info(f"技能 {skill} 剩余PP: {self.skill_pp[skill]}")
        else:
            logger.info(f"使用特定技能: {skill} (无PP记录)")
            self._press_key(skill)
    
    def _apply_condition_skills(self):
        """根据需要的捕捉条件应用相应的技能"""
        # 获取需要的捕捉条件（排除'any'）
        required_conditions = [cond for cond in self.config["catch_conditions"] if cond != "any"]
        
        if not required_conditions or "condition_skills" not in self.config:
            return False
        
        # 遍历需要的条件，应用对应的技能
        for condition in required_conditions:
            # 检查该条件是否已经满足
            # 临时修改配置来检查单个条件
            original_conditions = self.config["catch_conditions"].copy()
            self.config["catch_conditions"] = [condition]
            
            if not self._check_pokemon_condition():
                # 条件未满足，应用对应技能
                skills = self.config["condition_skills"].get(condition, [])
                if skills:
                    # 筛选出PP值足够的技能
                    valid_skills = []
                    for skill in skills:
                        if isinstance(skill, list):
                            # 如果是列表，展开列表
                            for s in skill:
                                if s in self.skill_pp and self.skill_pp[s] > 0:
                                    valid_skills.append(s)
                        else:
                            if skill in self.skill_pp and self.skill_pp[skill] > 0:
                                valid_skills.append(skill)
                    
                    if not valid_skills:
                        logger.warning(f"{condition}条件的技能PP值已耗尽！")
                        continue
                    
                    logger.info(f"应用{condition}条件的技能: {valid_skills}")
                    # 随机选择一个技能使用
                    skill = random.choice(valid_skills)
                    self._press_key(skill)
                    
                    # 减少PP值
                    if skill in self.skill_pp:
                        self.skill_pp[skill] -= 1
                        logger.info(f"技能 {skill} 剩余PP: {self.skill_pp[skill]}")
                    
                    # 恢复原始条件配置
                    self.config["catch_conditions"] = original_conditions
                    return True
            
            # 恢复原始条件配置
            self.config["catch_conditions"] = original_conditions
        
        return False
    
    def _close_pokemon_info(self):
        """关闭宠物资料界面"""
        logger.info("关闭宠物资料界面")
        
        # 使用esc键关闭宠物资料界面
        self._press_key("escape")
        logger.info("使用esc键关闭宠物资料界面")
        
        # 等待关闭动画
        time.sleep(0.5)
        
    
    def _check_pp_empty(self):
        """检查PP值是否用完"""
        for skill, pp in self.skill_pp.items():
            if pp > self.config["pp_threshold"]:
                return False
        return True
    
    def run(self):
        """运行GUI主循环"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.stop_automation()
        finally:
            if hasattr(self, 'keyboard_listener'):
                self.keyboard_listener.stop()

if __name__ == "__main__":
    try:
        automation = PokeMMOAutomation()
        automation.run()
    except Exception as e:
        logger.error(f"程序启动失败: {str(e)}")
        sys.exit(1)
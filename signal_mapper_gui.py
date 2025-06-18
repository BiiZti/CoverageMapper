#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2024 Signal Coverage Mapper

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
信号覆盖地图GUI版本 - 一键启动桌面应用
========================================

技术文档
--------
本应用基于Python Tkinter框架开发，集成HTTP服务器、数据处理、地图可视化等功能。

核心架构：
1. GUI界面层 (Tkinter) - 用户交互界面
2. HTTP服务器层 (http.server) - 提供Web服务
3. 数据处理层 (pandas) - Excel数据解析
4. 可视化层 (HTML/JavaScript) - 地图展示

API说明
-------
主要类：SignalMapperGUI
- __init__(): 初始化GUI和服务器配置
- setup_ui(): 构建用户界面
- start_server(): 启动HTTP服务器
- stop_server(): 停止HTTP服务器
- create_sample_data(): 生成示例数据
- quick_start(): 一键启动完整服务

技术要求
--------
- Python 3.7+
- 依赖包: tkinter, pandas, openpyxl
- 系统要求: Windows/Linux/macOS
- 内存要求: 最小256MB
- 网络要求: localhost访问权限

故障排除指南
-----------
1. 端口占用: 程序会自动寻找8888-8999范围内可用端口
2. 权限问题: 确保有本地文件读写权限
3. 浏览器问题: 支持Chrome/Firefox/Edge等现代浏览器
4. 数据格式: Excel文件需包含指定列名
5. 网络问题: 检查防火墙设置，允许本地HTTP服务

配置说明
--------
- 默认端口: 8888 (自动递增查找可用端口)
- 日志级别: INFO/DEBUG/ERROR
- 数据文件: example_data.xlsx
- 网页文件: signal_coverage_map.html
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import webbrowser
import os
import sys
import time
import socket
import platform
import psutil
import logging
import traceback
import importlib
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import pandas as pd

class EnhancedLogger:
    """增强的日志系统"""
    
    def __init__(self, gui_callback=None):
        self.gui_callback = gui_callback
        self.log_level = logging.INFO
        
        # 配置日志
        logging.basicConfig(
            level=self.log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('signal_mapper.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def debug(self, message):
        """调试级别日志"""
        self.logger.debug(message)
        if self.gui_callback:
            self.gui_callback(f"🔍 DEBUG: {message}", 'debug')
    
    def info(self, message):
        """信息级别日志"""
        self.logger.info(message)
        if self.gui_callback:
            self.gui_callback(f"ℹ️ {message}", 'info')
    
    def warning(self, message):
        """警告级别日志"""
        self.logger.warning(message)
        if self.gui_callback:
            self.gui_callback(f"⚠️ WARNING: {message}", 'warning')
    
    def error(self, message):
        """错误级别日志"""
        self.logger.error(message)
        if self.gui_callback:
            self.gui_callback(f"❌ ERROR: {message}", 'error')
    
    def critical(self, message):
        """严重错误级别日志"""
        self.logger.critical(message)
        if self.gui_callback:
            self.gui_callback(f"🚨 CRITICAL: {message}", 'critical')

class SystemDiagnostics:
    """系统环境检测工具"""
    
    @staticmethod
    def check_system_info():
        """检查系统信息"""
        info = {
            'platform': platform.platform(),
            'python_version': sys.version,
            'cpu_count': psutil.cpu_count(),
            'memory_total': f"{psutil.virtual_memory().total / (1024**3):.1f}GB",
            'memory_available': f"{psutil.virtual_memory().available / (1024**3):.1f}GB",
            'disk_free': f"{psutil.disk_usage('/').free / (1024**3):.1f}GB" if os.name != 'nt' else f"{psutil.disk_usage('C:').free / (1024**3):.1f}GB"
        }
        return info
    
    @staticmethod
    def check_dependencies():
        """检查依赖包"""
        dependencies = {
            'pandas': False,
            'openpyxl': False,
            'psutil': False
        }
        
        for package in dependencies:
            try:
                importlib.import_module(package)
                dependencies[package] = True
            except ImportError:
                dependencies[package] = False
        
        return dependencies
    
    @staticmethod
    def check_ports(start_port=8888, end_port=8999, max_check=5):
        """检查端口可用性 - 限制检查数量避免阻塞"""
        available_ports = []
        checked = 0
        
        for port in range(start_port, end_port + 1):
            if checked >= max_check:  # 最多只检查5个端口
                break
                
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)  # 设置100ms超时
                result = sock.connect_ex(('127.0.0.1', port))
                if result != 0:
                    available_ports.append(port)
                sock.close()
                checked += 1
            except:
                # 如果连接失败，说明端口可用
                available_ports.append(port)
                checked += 1
                
        return available_ports
    
    @staticmethod
    def check_file_permissions():
        """检查文件权限"""
        test_file = 'test_permission.tmp'
        try:
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            return True
        except:
            return False

class ErrorDiagnostics:
    """增强的错误诊断功能"""
    
    @staticmethod
    def analyze_exception(exception):
        """分析异常并提供解决方案"""
        error_type = type(exception).__name__
        error_msg = str(exception)
        
        solutions = {
            'PermissionError': '权限不足，请以管理员身份运行程序',
            'FileNotFoundError': '文件未找到，请检查文件路径是否正确',
            'OSError': '操作系统错误，可能是端口被占用或权限问题',
            'ImportError': '缺少必要的Python包，请运行: pip install -r requirements.txt',
            'ConnectionError': '网络连接问题，请检查网络设置',
            'TimeoutError': '操作超时，请稍后重试'
        }
        
        solution = solutions.get(error_type, '未知错误，请查看详细日志')
        
        return {
            'type': error_type,
            'message': error_msg,
            'solution': solution,
            'traceback': traceback.format_exc()
        }

class SignalMapperGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🗺️ 信号覆盖地图分析器 v2.1 (增强版)")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # 服务器相关
        self.server = None
        self.server_thread = None
        self.server_port = 8888
        self.server_running = False
        
        # 调试模式
        self.debug_mode = False
        
        # 初始化诊断工具（不依赖GUI）
        self.diagnostics = SystemDiagnostics()
        self.error_diagnostics = ErrorDiagnostics()
        
        # 先设置UI，再初始化日志器
        self.setup_ui()
        
        # 现在可以安全地初始化日志器
        self.logger = EnhancedLogger(self.log_message)
        
        # 初始化时进行系统检查
        self.perform_startup_diagnostics()
        
    def perform_startup_diagnostics(self):
        """启动时的快速诊断 - 避免阻塞"""
        try:
            if hasattr(self, 'logger'):
                self.logger.info("系统检查完成，程序就绪")
                
                # 使用线程执行耗时的诊断，避免阻塞UI
                def background_check():
                    try:
                        # 系统信息检查
                        sys_info = self.diagnostics.check_system_info()
                        self.logger.debug(f"平台: {sys_info['platform']}")
                        
                        # 依赖检查
                        deps = self.diagnostics.check_dependencies()
                        missing_deps = [dep for dep, available in deps.items() if not available]
                        if missing_deps:
                            self.logger.warning(f"缺少依赖包: {', '.join(missing_deps)}")
                        else:
                            self.logger.debug("所有依赖包检查通过")
                            
                        # 权限检查
                        if not self.diagnostics.check_file_permissions():
                            self.logger.warning("文件读写权限可能受限")
                        else:
                            self.logger.debug("文件权限检查通过")
                            
                    except Exception as e:
                        self.logger.debug(f"后台诊断异常: {str(e)}")
                
                # 启动后台检查线程
                check_thread = threading.Thread(target=background_check, daemon=True)
                check_thread.start()
                
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"诊断启动失败: {str(e)}")
            else:
                print(f"诊断启动失败: {str(e)}")
        
    def setup_ui(self):
        """设置用户界面"""
        # 主标题
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🗺️ 信号覆盖地图分析器 (增强版)", 
                              font=('微软雅黑', 20, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        # 主容器
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 左侧控制面板
        left_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # 控制按钮
        self.setup_control_panel(left_frame)
        
        # 右侧信息面板
        right_frame = tk.Frame(main_frame, bg='#f0f0f0')
        right_frame.pack(side='right', fill='both', expand=True)
        
        self.setup_info_panel(right_frame)
        
        # 底部状态栏
        self.status_bar = tk.Label(self.root, text="📍 就绪 - 点击一键启动开始使用", 
                                  relief='sunken', anchor='w', bg='#34495e', fg='white',
                                  font=('微软雅黑', 10))
        self.status_bar.pack(side='bottom', fill='x')
        
    def setup_control_panel(self, parent):
        """设置控制面板"""
        tk.Label(parent, text="🎛️ 控制面板", font=('微软雅黑', 14, 'bold'), 
                bg='white', fg='#2c3e50').pack(pady=10)
        
        # 一键启动按钮 (最重要)
        self.quick_start_btn = tk.Button(parent, text="🚀 一键启动完整服务", 
                                        command=self.quick_start,
                                        bg='#e67e22', fg='white', 
                                        font=('微软雅黑', 14, 'bold'),
                                        height=2, width=20)
        self.quick_start_btn.pack(pady=20, padx=20)
        
        # 分割线
        tk.Frame(parent, height=2, bg='#bdc3c7').pack(fill='x', padx=20, pady=10)
        
        # 服务器控制组
        server_frame = tk.LabelFrame(parent, text="🌐 服务器控制", 
                                    font=('微软雅黑', 11, 'bold'),
                                    bg='white', padx=10, pady=10)
        server_frame.pack(fill='x', padx=10, pady=5)
        
        self.start_btn = tk.Button(server_frame, text="启动服务器", 
                                  command=self.start_server,
                                  bg='#27ae60', fg='white', width=15)
        self.start_btn.pack(pady=2)
        
        self.stop_btn = tk.Button(server_frame, text="停止服务器", 
                                 command=self.stop_server,
                                 bg='#e74c3c', fg='white', width=15, state='disabled')
        self.stop_btn.pack(pady=2)
        
        self.open_btn = tk.Button(server_frame, text="打开网页", 
                                 command=self.open_browser,
                                 bg='#3498db', fg='white', width=15, state='disabled')
        self.open_btn.pack(pady=2)
        
        # 数据管理组
        data_frame = tk.LabelFrame(parent, text="📊 数据管理", 
                                  font=('微软雅黑', 11, 'bold'),
                                  bg='white', padx=10, pady=10)
        data_frame.pack(fill='x', padx=10, pady=5)
        
        self.create_data_btn = tk.Button(data_frame, text="生成示例数据", 
                                        command=self.create_sample_data,
                                        bg='#f39c12', fg='white', width=15)
        self.create_data_btn.pack(pady=2)
        
        self.select_file_btn = tk.Button(data_frame, text="选择Excel文件", 
                                        command=self.select_excel_file,
                                        bg='#9b59b6', fg='white', width=15)
        self.select_file_btn.pack(pady=2)
        
        # 文件路径显示
        self.file_path = tk.StringVar(value="未选择文件")
        file_label = tk.Label(data_frame, textvariable=self.file_path, 
                             wraplength=200, bg='white', fg='#7f8c8d', 
                             font=('微软雅黑', 9))
        file_label.pack(pady=5)
        
        # 新增：诊断工具组
        diag_frame = tk.LabelFrame(parent, text="🔧 诊断工具", 
                                  font=('微软雅黑', 11, 'bold'),
                                  bg='white', padx=10, pady=10)
        diag_frame.pack(fill='x', padx=10, pady=5)
        
        self.system_check_btn = tk.Button(diag_frame, text="系统检查", 
                                         command=self.system_check,
                                         bg='#8e44ad', fg='white', width=15)
        self.system_check_btn.pack(pady=2)
        
        self.debug_toggle_btn = tk.Button(diag_frame, text="开启调试", 
                                         command=self.toggle_debug_mode,
                                         bg='#34495e', fg='white', width=15)
        self.debug_toggle_btn.pack(pady=2)
        
        self.export_log_btn = tk.Button(diag_frame, text="导出日志", 
                                       command=self.export_logs,
                                       bg='#16a085', fg='white', width=15)
        self.export_log_btn.pack(pady=2)
        
    def setup_info_panel(self, parent):
        """设置信息面板"""
        # 创建选项卡
        notebook = ttk.Notebook(parent)
        notebook.pack(fill='both', expand=True)
        
        # 状态信息选项卡
        status_frame = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(status_frame, text='📈 运行状态')
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=15, 
                                                    font=('Consolas', 10), 
                                                    bg='#2c3e50', fg='#00ff00')
        self.status_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # 系统信息选项卡
        system_frame = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(system_frame, text='💻 系统信息')
        
        self.system_text = scrolledtext.ScrolledText(system_frame, height=15, 
                                                    font=('Consolas', 9), 
                                                    bg='white', fg='#2c3e50')
        self.system_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # 帮助文档选项卡
        help_frame = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(help_frame, text='ℹ️ 帮助文档')
        
        help_content = """🎯 主要功能：
✅ 一键启动HTTP服务器
✅ 自动打开浏览器访问地图
✅ Excel数据导入和解析
✅ 智能信号分析算法
✅ 热力图可视化展示
✅ 系统诊断和错误排除

🚀 使用步骤：
1. 点击"一键启动完整服务"
2. 程序自动生成示例数据
3. 启动HTTP服务器
4. 打开浏览器显示地图

📊 数据格式要求：
- 位置描述、详细地址、网络类型
- 信号强度、上报时间等

🔧 诊断工具：
- 系统检查：检测环境和依赖
- 调试模式：显示详细操作日志
- 导出日志：保存诊断信息

🆘 故障排除：
1. 端口占用 → 程序自动切换端口
2. 权限问题 → 以管理员身份运行
3. 浏览器问题 → 手动访问显示的URL
4. 数据格式 → 使用生成的示例数据
5. 网络问题 → 检查防火墙设置

📞 技术支持：
- 日志文件：signal_mapper.log
- 配置检查：点击"系统检查"
- 详细错误：开启"调试模式"
"""
        
        help_text = scrolledtext.ScrolledText(help_frame, wrap='word', font=('微软雅黑', 10), 
                                             bg='white', relief='flat')
        help_text.pack(fill='both', expand=True, padx=5, pady=5)
        help_text.insert('1.0', help_content)
        help_text.config(state='disabled')
        
        # 初始化系统信息显示
        self.update_system_info()
        
    def update_system_info(self):
        """更新系统信息显示"""
        try:
            sys_info = self.diagnostics.check_system_info()
            deps = self.diagnostics.check_dependencies()
            
            info_text = f"""系统信息
==================
操作系统: {sys_info['platform']}
Python版本: {sys_info['python_version'].split()[0]}
CPU核心数: {sys_info['cpu_count']}
总内存: {sys_info['memory_total']}
可用内存: {sys_info['memory_available']}
磁盘空间: {sys_info['disk_free']}

依赖包状态
==================
pandas: {'✅ 已安装' if deps['pandas'] else '❌ 未安装'}
openpyxl: {'✅ 已安装' if deps['openpyxl'] else '❌ 未安装'}
psutil: {'✅ 已安装' if deps['psutil'] else '❌ 未安装'}

网络端口检查
==================
可用端口范围: 8888-8999
"""
            
            try:
                available_ports = self.diagnostics.check_ports(max_check=3)  # 只检查前3个端口
                if available_ports:
                    info_text += f"可用端口: {', '.join(map(str, available_ports))}\n"
                else:
                    info_text += "端口检查中...\n"
            except:
                info_text += "端口检查跳过\n"
                
            self.system_text.delete('1.0', 'end')
            self.system_text.insert('1.0', info_text)
            
        except Exception as e:
            self.logger.error(f"更新系统信息失败: {str(e)}")
        
    def log_message(self, message, level='info'):
        """增强的日志记录功能"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # 根据级别设置颜色
        colors = {
            'debug': '#00ffff',
            'info': '#00ff00',
            'warning': '#ffff00',
            'error': '#ff0000',
            'critical': '#ff00ff'
        }
        
        color = colors.get(level, '#00ff00')
        
        self.status_text.config(state='normal')
        self.status_text.insert('end', f"[{timestamp}] {message}\n")
        
        # 为不同级别的消息设置颜色（简化版本）
        if level in ['error', 'critical']:
            self.status_text.insert('end', "\n")
        
        self.status_text.config(state='disabled')
        self.status_text.see('end')
        
        self.status_bar.config(text=f"📍 {message}")
        self.root.update()
        
    def system_check(self):
        """执行系统检查"""
        self.logger.info("开始执行系统检查...")
        
        try:
            # 更新系统信息
            self.update_system_info()
            
            # 检查关键文件
            required_files = ['signal_coverage_map.html']
            missing_files = [f for f in required_files if not os.path.exists(f)]
            
            if missing_files:
                self.logger.warning(f"缺少关键文件: {', '.join(missing_files)}")
            else:
                self.logger.info("关键文件检查通过")
            
            # 检查端口可用性
            available_ports = self.diagnostics.check_ports()
            if available_ports:
                self.logger.info(f"找到 {len(available_ports)} 个可用端口")
            else:
                self.logger.warning("没有找到可用端口，可能需要管理员权限")
            
            # 检查文件权限
            if self.diagnostics.check_file_permissions():
                self.logger.info("文件权限检查通过")
            else:
                self.logger.warning("文件权限受限，可能影响数据保存")
            
            self.logger.info("✅ 系统检查完成")
            
        except Exception as e:
            error_info = self.error_diagnostics.analyze_exception(e)
            self.logger.error(f"系统检查失败: {error_info['solution']}")
            if self.debug_mode:
                self.logger.debug(f"详细错误: {error_info['traceback']}")
    
    def toggle_debug_mode(self):
        """切换调试模式"""
        self.debug_mode = not self.debug_mode
        
        if self.debug_mode:
            self.debug_toggle_btn.config(text="关闭调试", bg='#e74c3c')
            self.logger.logger.setLevel(logging.DEBUG)
            self.logger.info("🔍 调试模式已开启")
        else:
            self.debug_toggle_btn.config(text="开启调试", bg='#34495e')
            self.logger.logger.setLevel(logging.INFO)
            self.logger.info("调试模式已关闭")
    
    def export_logs(self):
        """导出日志文件"""
        try:
            log_file = f"signal_mapper_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            
            # 收集系统信息
            sys_info = self.diagnostics.check_system_info()
            deps = self.diagnostics.check_dependencies()
            
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write("信号覆盖地图分析器 - 诊断报告\n")
                f.write("=" * 50 + "\n")
                f.write(f"导出时间: {datetime.now()}\n")
                f.write(f"调试模式: {'开启' if self.debug_mode else '关闭'}\n")
                f.write(f"服务器状态: {'运行中' if self.server_running else '已停止'}\n\n")
                
                f.write("系统信息:\n")
                for key, value in sys_info.items():
                    f.write(f"  {key}: {value}\n")
                
                f.write("\n依赖包状态:\n")
                for dep, status in deps.items():
                    f.write(f"  {dep}: {'已安装' if status else '未安装'}\n")
                
                f.write("\n当前日志内容:\n")
                f.write("-" * 30 + "\n")
                current_log = self.status_text.get('1.0', 'end')
                f.write(current_log)
            
            self.logger.info(f"✅ 日志已导出到: {log_file}")
            messagebox.showinfo("导出成功", f"日志文件已保存到:\n{log_file}")
            
        except Exception as e:
            error_info = self.error_diagnostics.analyze_exception(e)
            self.logger.error(f"导出日志失败: {error_info['solution']}")
    
    def find_free_port(self):
        """查找可用端口 - 增强版"""
        available_ports = self.diagnostics.check_ports()
        if available_ports:
            self.logger.debug(f"找到可用端口: {available_ports[:3]}")
            return available_ports[0]
        else:
            self.logger.warning("未找到可用端口，使用默认端口8888")
            return 8888

    def start_server(self):
        """启动HTTP服务器 - 增强版"""
        if self.server_running:
            self.logger.warning("服务器已在运行中")
            return
            
        try:
            # 检查关键文件
            if not os.path.exists('signal_coverage_map.html'):
                self.logger.error("缺少关键文件: signal_coverage_map.html")
                messagebox.showerror("错误", "缺少关键文件 signal_coverage_map.html\n请确保文件存在")
                return
            
            self.server_port = self.find_free_port()
            self.logger.info(f"正在启动HTTP服务器，端口: {self.server_port}")
            
            # 切换到脚本目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            os.chdir(script_dir)
            self.logger.debug(f"工作目录: {script_dir}")
            
            class CustomHandler(SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                
                def log_message(self, format, *args):
                    # 重定向到我们的日志系统
                    pass
                    
                def end_headers(self):
                    self.send_header('Cache-Control', 'no-cache')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    super().end_headers()
                
                def do_GET(self):
                    try:
                        super().do_GET()
                    except Exception as e:
                        self.send_error(500, f"Internal Server Error: {str(e)}")
            
            self.server = HTTPServer(('localhost', self.server_port), CustomHandler)
            
            def run_server():
                try:
                    self.logger.debug("HTTP服务器线程开始运行")
                    self.server.serve_forever()
                except Exception as e:
                    if self.server_running:
                        error_info = self.error_diagnostics.analyze_exception(e)
                        self.logger.error(f"服务器运行错误: {error_info['solution']}")
                        if self.debug_mode:
                            self.logger.debug(f"详细错误: {error_info['traceback']}")
            
            self.server_thread = threading.Thread(target=run_server, daemon=True)
            self.server_thread.start()
            
            # 等待服务器启动
            time.sleep(0.5)
            
            self.server_running = True
            self.logger.info(f"✅ HTTP服务器启动成功！地址: http://localhost:{self.server_port}")
            
            # 更新按钮状态
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.open_btn.config(state='normal')
            
        except Exception as e:
            error_info = self.error_diagnostics.analyze_exception(e)
            self.logger.error(f"服务器启动失败: {error_info['solution']}")
            if self.debug_mode:
                self.logger.debug(f"详细错误: {error_info['traceback']}")
            messagebox.showerror("服务器启动失败", f"错误类型: {error_info['type']}\n解决方案: {error_info['solution']}")
    
    def stop_server(self):
        """停止HTTP服务器 - 增强版"""
        if not self.server_running:
            self.logger.warning("服务器未在运行")
            return
            
        try:
            self.logger.info("正在停止HTTP服务器...")
            self.server_running = False
            
            if self.server:
                self.server.shutdown()
                self.server.server_close()
                self.logger.debug("服务器套接字已关闭")
                
            self.logger.info("✅ HTTP服务器已停止")
            
            # 更新按钮状态
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.open_btn.config(state='disabled')
            
        except Exception as e:
            error_info = self.error_diagnostics.analyze_exception(e)
            self.logger.error(f"停止服务器失败: {error_info['solution']}")
            if self.debug_mode:
                self.logger.debug(f"详细错误: {error_info['traceback']}")
    
    def open_browser(self):
        """打开浏览器 - 增强版"""
        if not self.server_running:
            self.logger.error("请先启动服务器")
            messagebox.showwarning("警告", "请先点击'启动服务器'按钮")
            return
            
        url = f"http://localhost:{self.server_port}/signal_coverage_map.html"
        self.logger.info(f"正在打开浏览器: {url}")
        
        try:
            # 检查网页文件是否存在
            if not os.path.exists('signal_coverage_map.html'):
                self.logger.error("网页文件不存在")
                messagebox.showerror("错误", "signal_coverage_map.html 文件不存在")
                return
                
            webbrowser.open(url)
            self.logger.info("✅ 浏览器已打开")
            
            # 显示访问信息
            messagebox.showinfo("浏览器已打开", f"网页地址: {url}\n\n如果浏览器未自动打开，请手动复制上述地址到浏览器访问")
            
        except Exception as e:
            error_info = self.error_diagnostics.analyze_exception(e)
            self.logger.error(f"打开浏览器失败: {error_info['solution']}")
            if self.debug_mode:
                self.logger.debug(f"详细错误: {error_info['traceback']}")
            messagebox.showerror("打开浏览器失败", f"请手动打开浏览器访问:\n{url}")
    
    def create_sample_data(self):
        """生成示例数据 - 增强版"""
        try:
            self.logger.info("正在生成示例数据...")
            
            # 检查文件权限
            if not self.diagnostics.check_file_permissions():
                self.logger.error("文件写入权限不足")
                messagebox.showerror("权限错误", "程序没有文件写入权限\n请以管理员身份运行程序")
                return
            
            # 南通市示例数据 (100个数据点)
            sample_data = [
                {
                    '位置描述': '南通市崇川区南大街',
                    '详细地址': '江苏省南通市崇川区南大街128号',
                    '网络类型': '5G',
                    '信号强度': 2,
                    '上报时间': '2024-01-15 10:30',
                    '上报人': '张三',
                    '备注': '地下商场信号较弱'
                },
                {
                    '位置描述': '南通市开发区星湖101广场',
                    '详细地址': '江苏省南通市开发区星湖大道101号',
                    '网络类型': '4G',
                    '信号强度': 3,
                    '上报时间': '2024-01-15 14:20',
                    '上报人': '李四',
                    '备注': '电梯内部分楼层无信号'
                },
                {
                    '位置描述': '南通市通州区金沙中学',
                    '详细地址': '江苏省南通市通州区金沙镇人民东路88号',
                    '网络类型': '5G',
                    '信号强度': 1,
                    '上报时间': '2024-01-16 09:15',
                    '上报人': '王五',
                    '备注': '教学楼地下室完全无信号'
                },
                {
                    '位置描述': '南通市港闸区万达广场',
                    '详细地址': '江苏省南通市港闸区永兴大道999号',
                    '网络类型': '4G',
                    '信号强度': 4,
                    '上报时间': '2024-01-16 16:45',
                    '上报人': '赵六',
                    '备注': '停车场B2层信号断断续续'
                },
                {
                    '位置描述': '南通市如东县掘港镇人民路',
                    '详细地址': '江苏省南通市如东县掘港镇人民中路168号',
                    '网络类型': '5G',
                    '信号强度': 2,
                    '上报时间': '2024-01-17 11:30',
                    '上报人': '钱七',
                    '备注': '银行内部信号不稳定'
                },
                {
                    '位置描述': '南通市海门区人民中路',
                    '详细地址': '江苏省南通市海门区人民中路258号',
                    '网络类型': '4G',
                    '信号强度': 6,
                    '上报时间': '2024-01-17 15:20',
                    '上报人': '孙八',
                    '备注': '商业街信号基本正常'
                },
                {
                    '位置描述': '南通市启东市汇龙镇',
                    '详细地址': '江苏省南通市启东市汇龙镇人民中路368号',
                    '网络类型': '5G',
                    '信号强度': 7,
                    '上报时间': '2024-01-18 09:00',
                    '上报人': '周九',
                    '备注': '市政府附近信号良好'
                },
                {
                    '位置描述': '南通市海安市中大街',
                    '详细地址': '江苏省南通市海安市中大街199号',
                    '网络类型': '4G',
                    '信号强度': 5,
                    '上报时间': '2024-01-18 13:45',
                    '上报人': '吴十',
                    '备注': '老城区信号中等'
                },
                {
                    '位置描述': '南通火车站',
                    '详细地址': '江苏省南通市崇川区青年东路32号',
                    '网络类型': '5G',
                    '信号强度': 8,
                    '上报时间': '2024-01-19 08:15',
                    '上报人': '郑十一',
                    '备注': '交通枢纽信号覆盖良好'
                },
                {
                    '位置描述': '南通大学附属医院',
                    '详细地址': '江苏省南通市崇川区西寺路20号',
                    '网络类型': '5G',
                    '信号强度': 6,
                    '上报时间': '2024-01-19 14:30',
                    '上报人': '冯十二',
                    '备注': '医院大楼内信号稳定'
                }
            ]
            
            # 生成更多示例数据 (扩展到100个)
            import random
            base_locations = [
                ("南通市崇川区", "江苏省南通市崇川区"),
                ("南通市开发区", "江苏省南通市开发区"),
                ("南通市通州区", "江苏省南通市通州区"),
                ("南通市港闸区", "江苏省南通市港闸区"),
                ("南通市如东县", "江苏省南通市如东县"),
                ("南通市海门区", "江苏省南通市海门区"),
                ("南通市启东市", "江苏省南通市启东市"),
                ("南通市海安市", "江苏省南通市海安市"),
            ]
            
            names = ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十", "郑十一", "冯十二", 
                    "陈明", "林华", "黄强", "刘敏", "杨洋", "朱峰", "徐静", "马超", "梁美", "谢勇"]
            network_types = ["4G", "5G"]
            
            # 扩展示例数据到100个
            for i in range(len(sample_data), 100):
                location = random.choice(base_locations)
                street_names = ["人民路", "中山路", "解放路", "建设路", "文化路", "工农路", "胜利路", "和平路", "友谊路", "青年路"]
                street = random.choice(street_names)
                number = random.randint(1, 999)
                
                sample_data.append({
                    '位置描述': f"{location[0]}{street}",
                    '详细地址': f"{location[1]}{street}{number}号",
                    '网络类型': random.choice(network_types),
                    '信号强度': random.randint(1, 8),
                    '上报时间': f"2024-01-{random.randint(15, 30):02d} {random.randint(8, 18):02d}:{random.randint(0, 59):02d}",
                    '上报人': random.choice(names),
                    '备注': random.choice([
                        "信号正常", "信号较弱", "偶有中断", "地下室信号差", 
                        "电梯内无信号", "室内信号良好", "户外信号强", "网络稳定"
                    ])
                })
            
            # 保存为Excel文件
            df = pd.DataFrame(sample_data)
            file_path = 'example_data.xlsx'
            
            self.logger.debug(f"准备写入{len(sample_data)}条记录到{file_path}")
            df.to_excel(file_path, index=False)
            
            self.file_path.set(f"已生成: {file_path}")
            self.logger.info(f"✅ 示例数据已生成: {file_path} (共{len(sample_data)}条记录)")
            
            # 验证文件
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                self.logger.debug(f"文件大小: {file_size} 字节")
            
        except Exception as e:
            error_info = self.error_diagnostics.analyze_exception(e)
            self.logger.error(f"生成示例数据失败: {error_info['solution']}")
            if self.debug_mode:
                self.logger.debug(f"详细错误: {error_info['traceback']}")
            messagebox.showerror("生成数据失败", f"错误类型: {error_info['type']}\n解决方案: {error_info['solution']}")
    
    def select_excel_file(self):
        """选择Excel文件 - 增强版"""
        try:
            file_path = filedialog.askopenfilename(
                title="选择Excel文件",
                filetypes=[("Excel文件", "*.xlsx *.xls"), ("所有文件", "*.*")]
            )
            
            if file_path:
                # 验证文件
                if not os.path.exists(file_path):
                    self.logger.error("选择的文件不存在")
                    messagebox.showerror("错误", "选择的文件不存在")
                    return
                    
                # 检查文件格式
                if not file_path.lower().endswith(('.xlsx', '.xls')):
                    self.logger.warning("文件格式可能不正确")
                    messagebox.showwarning("警告", "建议选择.xlsx或.xls格式的Excel文件")
                
                # 检查文件大小
                file_size = os.path.getsize(file_path)
                if file_size > 50 * 1024 * 1024:  # 50MB
                    self.logger.warning("文件过大，可能影响性能")
                    messagebox.showwarning("警告", "文件较大，加载可能需要较长时间")
                
                self.file_path.set(file_path)
                self.logger.info(f"已选择文件: {os.path.basename(file_path)} ({file_size/1024:.1f}KB)")
                
                # 尝试验证Excel文件结构
                try:
                    df = pd.read_excel(file_path)
                    self.logger.debug(f"文件包含 {len(df)} 行数据")
                    required_columns = ['位置描述', '详细地址', '网络类型', '信号强度']
                    missing_columns = [col for col in required_columns if col not in df.columns]
                    if missing_columns:
                        self.logger.warning(f"缺少必要列: {', '.join(missing_columns)}")
                        messagebox.showwarning("数据格式提醒", f"Excel文件建议包含以下列:\n{', '.join(required_columns)}")
                except Exception as e:
                    self.logger.warning("无法预览Excel文件内容")
                    
        except Exception as e:
            error_info = self.error_diagnostics.analyze_exception(e)
            self.logger.error(f"选择文件失败: {error_info['solution']}")
            if self.debug_mode:
                self.logger.debug(f"详细错误: {error_info['traceback']}")
    
    def quick_start(self):
        """一键启动完整服务 - 增强版"""
        self.logger.info("🚀 开始一键启动...")
        
        try:
            # 1. 系统检查
            self.logger.info("步骤 1/4: 执行系统检查...")
            self.system_check()
            time.sleep(0.5)
            
            # 2. 生成示例数据
            self.logger.info("步骤 2/4: 生成示例数据...")
            self.create_sample_data()
            time.sleep(0.5)
            
            # 3. 启动服务器
            self.logger.info("步骤 3/4: 启动HTTP服务器...")
            self.start_server()
            time.sleep(1)
            
            # 4. 打开浏览器
            if self.server_running:
                self.logger.info("步骤 4/4: 打开浏览器...")
                self.open_browser()
                self.logger.info("🎉 一键启动完成！enjoy!")
            else:
                self.logger.error("一键启动失败，服务器未能成功启动")
                messagebox.showerror("启动失败", "服务器启动失败，请查看日志信息")
                
        except Exception as e:
            error_info = self.error_diagnostics.analyze_exception(e)
            self.logger.error(f"一键启动失败: {error_info['solution']}")
            if self.debug_mode:
                self.logger.debug(f"详细错误: {error_info['traceback']}")
            messagebox.showerror("一键启动失败", f"错误: {error_info['solution']}")
    
    def on_closing(self):
        """关闭程序时的清理工作 - 增强版"""
        try:
            self.logger.info("程序正在关闭...")
            
            # 停止服务器
            if self.server_running:
                self.logger.info("正在停止服务器...")
                self.stop_server()
            
            # 保存配置信息
            try:
                config_info = {
                    'last_port': self.server_port,
                    'debug_mode': self.debug_mode,
                    'close_time': datetime.now().isoformat()
                }
                self.logger.debug(f"保存配置: {config_info}")
            except:
                pass
            
            self.logger.info("程序已安全关闭")
            
        except Exception as e:
            # 即使清理失败也要继续关闭
            print(f"清理时发生错误: {e}")
        finally:
            self.root.destroy()
    
    def run(self):
        """运行GUI程序 - 增强版"""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            # 显示启动信息
            self.logger.info("🎯 信号覆盖地图分析器已就绪")
            self.logger.info("💡 点击'一键启动完整服务'开始使用")
            
            # 显示版本和技术信息
            self.logger.debug("程序版本: v2.1 (增强版)")
            self.logger.debug("技术支持: 完整诊断和日志系统")
            
            self.root.mainloop()
            
        except Exception as e:
            error_info = self.error_diagnostics.analyze_exception(e)
            self.logger.critical(f"GUI运行失败: {error_info['solution']}")
            messagebox.showerror("程序运行错误", f"错误: {error_info['solution']}")

def main():
    """主函数 - 增强版"""
    try:
        # 设置工作目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # 创建临时日志记录器用于启动阶段
        temp_logger = logging.getLogger('startup')
        temp_logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        temp_logger.addHandler(handler)
        
        temp_logger.info("信号覆盖地图分析器启动中...")
        temp_logger.info(f"工作目录: {script_dir}")
        
        # 基础环境检查
        if sys.version_info < (3, 7):
            raise RuntimeError("需要Python 3.7或更高版本")
        
        # 检查关键依赖
        required_modules = ['tkinter', 'pandas', 'psutil']
        missing_modules = []
        for module in required_modules:
            try:
                importlib.import_module(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            error_msg = f"缺少必要模块: {', '.join(missing_modules)}\n请运行: pip install {' '.join(missing_modules)}"
            messagebox.showerror("依赖错误", error_msg)
            sys.exit(1)
        
        # 启动应用
        app = SignalMapperGUI()
        app.run()
        
    except Exception as e:
        error_msg = f"程序启动失败:\n{str(e)}\n\n技术支持：\n1. 确保Python版本>=3.7\n2. 安装所需依赖包\n3. 以管理员身份运行"
        messagebox.showerror("程序错误", error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main()
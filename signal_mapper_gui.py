#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
信号覆盖地图GUI版本 - 一键启动桌面应用
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import webbrowser
import os
import sys
import time
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
import pandas as pd
from datetime import datetime

class SignalMapperGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🗺️ 信号覆盖地图分析器 v2.0")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # 服务器相关
        self.server = None
        self.server_thread = None
        self.server_port = 8888
        self.server_running = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 主标题
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🗺️ 信号覆盖地图分析器", 
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
        
    def setup_info_panel(self, parent):
        """设置信息面板"""
        # 状态信息
        status_frame = tk.LabelFrame(parent, text="📈 运行状态", 
                                    font=('微软雅黑', 12, 'bold'),
                                    bg='#f0f0f0', fg='#2c3e50')
        status_frame.pack(fill='x', pady=(0, 10))
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=10, 
                                                    font=('Consolas', 10), 
                                                    bg='#2c3e50', fg='#00ff00')
        self.status_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # 功能说明
        info_frame = tk.LabelFrame(parent, text="ℹ️ 使用说明", 
                                  font=('微软雅黑', 12, 'bold'),
                                  bg='#f0f0f0', fg='#2c3e50')
        info_frame.pack(fill='both', expand=True)
        
        info_content = """🎯 主要功能：
✅ 一键启动HTTP服务器
✅ 自动打开浏览器访问地图
✅ Excel数据导入和解析
✅ 智能信号分析算法
✅ 热力图可视化展示

🚀 使用步骤：
1. 点击"一键启动完整服务"
2. 程序自动生成示例数据
3. 启动HTTP服务器
4. 打开浏览器显示地图

📊 数据格式要求：
位置描述、详细地址、网络类型、信号强度、上报时间等

🔧 技术特性：
- 高德地图API集成
- 多算法融合分析
- 响应式Web界面
- 实时数据处理"""
        
        info_text = tk.Text(info_frame, wrap='word', font=('微软雅黑', 10), 
                           bg='white', relief='flat')
        info_text.pack(fill='both', expand=True, padx=5, pady=5)
        info_text.insert('1.0', info_content)
        info_text.config(state='disabled')
        
    def log_message(self, message, level='info'):
        """记录日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.status_text.config(state='normal')
        self.status_text.insert('end', f"[{timestamp}] {message}\n")
        self.status_text.config(state='disabled')
        self.status_text.see('end')
        
        self.status_bar.config(text=f"📍 {message}")
        self.root.update()
        
    def find_free_port(self):
        """查找可用端口"""
        for port in range(8888, 9000):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(('localhost', port))
                sock.close()
                return port
            except:
                continue
        return 8888
    
    def start_server(self):
        """启动HTTP服务器"""
        if self.server_running:
            self.log_message("服务器已在运行中")
            return
            
        try:
            self.server_port = self.find_free_port()
            self.log_message(f"正在启动HTTP服务器，端口: {self.server_port}")
            
            # 切换到脚本目录
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            
            class CustomHandler(SimpleHTTPRequestHandler):
                def log_message(self, format, *args):
                    pass
                    
                def end_headers(self):
                    self.send_header('Cache-Control', 'no-cache')
                    super().end_headers()
            
            self.server = HTTPServer(('localhost', self.server_port), CustomHandler)
            
            def run_server():
                try:
                    self.server.serve_forever()
                except Exception as e:
                    if self.server_running:
                        self.log_message(f"服务器错误: {str(e)}")
            
            self.server_thread = threading.Thread(target=run_server, daemon=True)
            self.server_thread.start()
            
            self.server_running = True
            self.log_message(f"✅ HTTP服务器启动成功！地址: http://localhost:{self.server_port}")
            
            # 更新按钮状态
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.open_btn.config(state='normal')
            
        except Exception as e:
            self.log_message(f"❌ 服务器启动失败: {str(e)}")
            messagebox.showerror("错误", f"服务器启动失败:\n{str(e)}")
    
    def stop_server(self):
        """停止HTTP服务器"""
        if not self.server_running:
            return
            
        try:
            self.log_message("正在停止HTTP服务器...")
            self.server_running = False
            
            if self.server:
                self.server.shutdown()
                self.server.server_close()
                
            self.log_message("✅ HTTP服务器已停止")
            
            # 更新按钮状态
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.open_btn.config(state='disabled')
            
        except Exception as e:
            self.log_message(f"❌ 停止服务器时出错: {str(e)}")
    
    def open_browser(self):
        """打开浏览器"""
        if not self.server_running:
            self.log_message("❌ 请先启动服务器")
            return
            
        url = f"http://localhost:{self.server_port}/signal_coverage_map.html"
        self.log_message(f"🌐 正在打开浏览器: {url}")
        
        try:
            webbrowser.open(url)
            self.log_message("✅ 浏览器已打开")
        except Exception as e:
            self.log_message(f"❌ 打开浏览器失败: {str(e)}")
    
    def create_sample_data(self):
        """生成示例数据"""
        try:
            self.log_message("📝 正在生成示例数据...")
            
            # 南通市示例数据
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
            
            # 保存为Excel文件
            df = pd.DataFrame(sample_data)
            file_path = 'example_data.xlsx'
            df.to_excel(file_path, index=False)
            
            self.file_path.set(f"已生成: {file_path}")
            self.log_message(f"✅ 示例数据已生成: {file_path}")
            
        except Exception as e:
            self.log_message(f"❌ 生成示例数据失败: {str(e)}")
            messagebox.showerror("错误", f"生成示例数据失败:\n{str(e)}")
    
    def select_excel_file(self):
        """选择Excel文件"""
        file_path = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=[("Excel文件", "*.xlsx *.xls"), ("所有文件", "*.*")]
        )
        
        if file_path:
            self.file_path.set(file_path)
            self.log_message(f"✅ 已选择文件: {os.path.basename(file_path)}")
    
    def quick_start(self):
        """一键启动完整服务"""
        self.log_message("🚀 开始一键启动...")
        
        # 1. 生成示例数据
        self.create_sample_data()
        time.sleep(0.5)
        
        # 2. 启动服务器
        self.start_server()
        time.sleep(1)
        
        # 3. 打开浏览器
        if self.server_running:
            self.open_browser()
            self.log_message("🎉 一键启动完成！enjoy!")
        else:
            self.log_message("❌ 一键启动失败，请检查服务器状态")
    
    def on_closing(self):
        """关闭程序时的清理工作"""
        if self.server_running:
            self.stop_server()
        self.root.destroy()
    
    def run(self):
        """运行GUI程序"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.log_message("🎯 信号覆盖地图分析器已就绪")
        self.log_message("💡 点击'一键启动完整服务'开始使用")
        self.root.mainloop()

def main():
    """主函数"""
    try:
        # 设置工作目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        app = SignalMapperGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("程序错误", f"程序启动失败:\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
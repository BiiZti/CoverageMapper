#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信号覆盖地图分析器 - 主启动程序
==============================

从项目根目录启动GUI应用程序的入口点。

使用方法:
    python main.py
    
或双击运行（Windows）。

作者: Signal Coverage Mapper Team
版本: v2.1
许可: MIT License
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """主函数 - 启动GUI应用程序"""
    try:
        from signal_mapper_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保所有依赖包已正确安装")
        print("运行: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
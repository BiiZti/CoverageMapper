# -*- coding: utf-8 -*-
"""
信号覆盖地图分析器 - 配置文件模板
=====================================

安全配置说明：
1. 请将此文件复制为 config.py
2. 在 config.py 中填入您的真实API密钥
3. 确保 config.py 已添加到 .gitignore 文件中
4. 不要将真实API密钥提交到版本控制系统

API密钥申请地址：
- 高德地图开放平台：https://developer.amap.com/
- 申请步骤：注册账号 → 创建应用 → 添加Key → 选择"Web服务API"
"""

# ================================
# API配置 - 高德地图API密钥
# ================================

# 注意：这里是示例配置，请替换为您的真实API密钥
# 服务端API密钥（用于地理编码等后端调用）
AMAP_API_KEY = "您的高德地图服务端API密钥"

# JavaScript API密钥（用于前端地图显示）
AMAP_JS_KEY = "您的高德地图JavaScript_API密钥"

# ================================
# 应用配置
# ================================

# 应用基本信息
APP_NAME = "信号覆盖地图分析器"
APP_VERSION = "2.1"
APP_DESCRIPTION = "基于高德地图的信号盲区分析工具"

# 服务器配置
SERVER_HOST = "localhost"
SERVER_PORT_START = 8888  # 起始端口，程序会自动寻找可用端口
SERVER_PORT_END = 8999    # 结束端口

# 数据文件配置
DEFAULT_EXCEL_FILE = "example_data.xlsx"
DEFAULT_HTML_FILE = "signal_coverage_map.html"
LOG_FILE = "signal_mapper.log"

# ================================
# 安全配置
# ================================

# 是否启用调试模式（生产环境建议设置为False）
DEBUG_MODE = True

# 日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL）
LOG_LEVEL = "INFO"

# API调用限制
API_RATE_LIMIT = 100  # 每秒最大API调用次数
API_TIMEOUT = 10      # API超时时间（秒）

# ================================
# 地图配置
# ================================

# 默认地图中心点（南通市）
DEFAULT_MAP_CENTER = {
    "latitude": 32.0307,
    "longitude": 120.8664,
    "zoom": 11
}

# 地图样式配置
MAP_CONFIG = {
    "style": "normal",  # 地图样式：normal/satellite/street
    "show_traffic": True,  # 是否显示实时路况
    "show_buildings": True,  # 是否显示建筑物
}

# ================================
# 数据配置
# ================================

# 示例数据生成配置
SAMPLE_DATA_CONFIG = {
    "count": 100,  # 生成数据点数量
    "area": "南通市",  # 数据覆盖区域
    "networks": ["5G", "4G", "3G"],  # 支持的网络类型
    "signal_range": [1, 10],  # 信号强度范围
}

# Excel文件列名映射
EXCEL_COLUMNS = {
    "location": "位置描述",
    "address": "详细地址", 
    "network": "网络类型",
    "signal": "信号强度",
    "time": "上报时间",
    "reporter": "上报人",
    "note": "备注"
}

# ================================
# 环境变量配置
# ================================

# 支持从环境变量读取配置（优先级高于文件配置）
import os

# 从环境变量读取API密钥
AMAP_API_KEY = os.getenv("AMAP_API_KEY", AMAP_API_KEY)
AMAP_JS_KEY = os.getenv("AMAP_JS_KEY", AMAP_JS_KEY)

# 从环境变量读取其他配置
DEBUG_MODE = os.getenv("DEBUG_MODE", str(DEBUG_MODE)).lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", LOG_LEVEL)

# ================================
# 配置验证
# ================================

def validate_config():
    """验证配置的有效性"""
    errors = []
    
    # 检查API密钥
    if not AMAP_API_KEY or AMAP_API_KEY == "您的高德地图服务端API密钥":
        errors.append("请配置有效的高德地图服务端API密钥 (AMAP_API_KEY)")
    
    if not AMAP_JS_KEY or AMAP_JS_KEY == "您的高德地图JavaScript_API密钥":
        errors.append("请配置有效的高德地图JavaScript API密钥 (AMAP_JS_KEY)")
    
    # 检查端口范围
    if SERVER_PORT_START >= SERVER_PORT_END:
        errors.append("服务器端口范围配置错误")
    
    # 检查文件路径
    if not DEFAULT_HTML_FILE.endswith('.html'):
        errors.append("HTML文件路径配置错误")
    
    if errors:
        print("配置验证失败：")
        for error in errors:
            print(f"  - {error}")
        return False
    
    return True

# ================================
# 配置加载函数
# ================================

def load_config():
    """加载并验证配置"""
    if not validate_config():
        print("\n请参考以下步骤配置API密钥：")
        print("1. 访问高德地图开放平台：https://developer.amap.com/")
        print("2. 注册账号并创建应用")
        print("3. 添加Key，选择'Web服务API'")
        print("4. 将API密钥填入config.py文件")
        print("5. 确保config.py已添加到.gitignore文件中")
        return False
    
    print("✅ 配置验证通过")
    return True

if __name__ == "__main__":
    load_config() 
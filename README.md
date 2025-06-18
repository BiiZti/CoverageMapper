# 🗺️ 信号覆盖地图分析器 (CoverageMapper)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/your-username/CoverageMapper)

一个专业的信号覆盖数据分析和可视化工具，支持从Excel数据生成交互式热力图，帮助分析通信信号盲区分布和优化网络覆盖。

## ✨ 主要特性

🎯 **一键启动**: 自动化的完整工作流程  
📊 **数据导入**: 支持Excel格式的信号数据  
🗺️ **地图可视化**: 基于高德地图的交互式热力图  
🔥 **热力分析**: 直观显示信号强度分布  
📍 **标记点**: 精确显示监测点位置  
🎛️ **筛选功能**: 支持按网络类型、信号强度筛选  
📈 **智能分析**: K-means聚类和盲区检测  
🔧 **系统诊断**: 完整的故障排除和日志系统  
🚀 **企业级**: 增强的错误处理和技术支持

## 🏗️ 项目结构

```
CoverageMapper/
├── 📁 src/                     # 源代码目录
│   ├── signal_mapper_gui.py    # 主GUI程序
│   ├── signal_mapper.py        # 核心业务逻辑
│   └── generate_amap_html.py    # HTML生成模块
├── 📁 static/                  # 静态文件目录
│   └── signal_coverage_map.html # 生成的地图网页
├── 📁 data/                    # 数据文件目录
│   ├── example_data.xlsx       # 示例数据
│   └── signal_mapper.log       # 日志文件
├── 📁 docs/                    # 文档目录
│   ├── TECHNICAL_DOCUMENTATION.md
│   ├── SECURITY_GUIDE.md
│   ├── CONTRIBUTING.md
│   └── CLA.md
├── 📁 scripts/                 # 脚本目录
│   ├── start_gui.bat           # Windows启动脚本
│   └── 创建桌面快捷方式.bat    # 快捷方式脚本
├── 📁 .github/                 # GitHub配置
├── main.py                     # 主启动程序
├── requirements.txt            # 依赖清单
├── config_template.py          # 配置模板
└── README.md                   # 项目说明
```

## 🚀 快速开始

### 方法一: 一键启动 (推荐)

1. **下载项目**
   ```bash
   git clone https://github.com/your-username/CoverageMapper.git
   cd CoverageMapper
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **启动程序**
   ```bash
   python main.py
   ```
   
   或者在Windows上双击运行 `scripts/start_gui.bat`

4. **使用应用**
   - 点击 "🚀 一键启动完整服务"
   - 程序自动生成示例数据、启动服务器、打开浏览器

### 方法二: 分步操作

1. **生成示例数据**: 点击"生成示例数据"按钮
2. **启动服务器**: 点击"启动服务器"按钮  
3. **打开网页**: 点击"打开网页"按钮
4. **查看地图**: 在浏览器中分析信号覆盖情况

## 📊 数据格式

Excel文件应包含以下列：

| 列名 | 类型 | 说明 | 示例 |
|------|------|------|------|
| 位置描述 | 文本 | 位置简要描述 | "南通市崇川区南大街" |
| 详细地址 | 文本 | 完整地址信息 | "江苏省南通市崇川区南大街128号" |
| 网络类型 | 文本 | 网络类型 | "4G" 或 "5G" |
| 信号强度 | 数字 | 信号强度等级 | 1-8 (1=无信号, 8=信号excellent) |
| 上报时间 | 日期 | 数据上报时间 | "2024-01-15 10:30" |
| 上报人 | 文本 | 数据上报人员 | "张三" |
| 备注 | 文本 | 其他备注信息 | "地下商场信号较弱" |

## 🔧 功能详解

### 核心功能
- **📍 地图展示**: 基于高德地图的专业地图服务
- **🔥 热力图**: 根据信号强度生成直观的热力分布
- **📌 标记点**: 显示具体的监测点位置和详细信息
- **🎛️ 筛选器**: 支持按网络类型、信号强度范围筛选数据
- **📊 智能分析**: 
  - 基础统计分析
  - K-means聚类分析
  - 信号盲区检测
  - 信号分布分析
  - 覆盖质量评估
  - 优化建议生成

### 技术特性
- **🔍 系统诊断**: 自动检测系统环境和依赖
- **📝 五级日志**: DEBUG/INFO/WARNING/ERROR/CRITICAL
- **⚡ 错误恢复**: 智能异常分析和解决方案提示
- **🛡️ 权限检查**: 自动检测文件权限和端口可用性
- **📊 性能监控**: 实时系统资源监控

## 🛠️ 高级配置

### 环境变量设置

创建 `.env` 文件配置：
```env
# 高德地图API配置
AMAP_WEB_KEY=your_web_api_key_here
AMAP_WEB_SECRET=your_web_secret_here

# 服务器配置
SERVER_HOST=localhost
SERVER_PORT=8888
DEBUG_MODE=false

# 数据文件路径
DATA_FILE_PATH=data/example_data.xlsx
HTML_OUTPUT_PATH=static/signal_coverage_map.html
LOG_FILE_PATH=data/signal_mapper.log
```

### 自定义配置

编辑 `config_template.py`:
```python
# API配置
AMAP_WEB_KEY = "your_api_key"
AMAP_WEB_SECRET = "your_secret"

# 文件路径
DEFAULT_EXCEL_FILE = "data/example_data.xlsx"
DEFAULT_HTML_FILE = "static/signal_coverage_map.html"
LOG_FILE = "data/signal_mapper.log"

# 地图配置
DEFAULT_CENTER = [120.8644, 32.0072]  # 南通市中心
DEFAULT_ZOOM = 11
```

## 🔍 故障排除

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| 🚫 服务器启动失败 | 检查端口占用，程序会自动切换可用端口 |
| 📂 文件权限错误 | 以管理员身份运行程序 |
| 🌐 浏览器未打开 | 手动复制显示的URL到浏览器 |
| 📊 数据格式错误 | 使用生成的示例数据作为模板 |
| 🔑 API密钥问题 | 在config_template.py中配置有效的高德地图API密钥 |

### 诊断工具

程序内置了完整的诊断工具：

1. **系统检查**: 检测Python环境、依赖包、文件权限
2. **调试模式**: 开启详细的操作日志
3. **日志导出**: 导出完整的诊断报告
4. **错误分析**: 智能错误分析和解决方案提示

## 📈 性能优化

- **内存优化**: 大数据集分批处理，避免内存溢出
- **渲染优化**: 热力图数据聚合，提升渲染性能  
- **网络优化**: 本地HTTP服务器，避免跨域问题
- **缓存机制**: 智能缓存地理编码结果

## 🤝 参与贡献

我们欢迎任何形式的贡献！请查看 [CONTRIBUTING.md](docs/CONTRIBUTING.md) 了解详细信息。

### 贡献类型
- 🐛 Bug修复
- ✨ 新功能开发  
- 📚 文档改进
- 🧪 测试用例
- 🎨 界面优化

## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源协议。

## 🙏 致谢

- [高德地图开放平台](https://lbs.amap.com/) - 提供地图服务
- [Pandas](https://pandas.pydata.org/) - 数据处理
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI界面
- [OpenPyXL](https://openpyxl.readthedocs.io/) - Excel文件处理

## 📞 支持

- 📧 邮箱: support@coveragemapper.com
- 🐛 问题反馈: [GitHub Issues](https://github.com/your-username/CoverageMapper/issues)
- 📖 文档: [技术文档](docs/TECHNICAL_DOCUMENTATION.md)
- 🔒 安全: [安全指南](docs/SECURITY_GUIDE.md)

---

**�� 让网络覆盖分析变得简单高效！** 
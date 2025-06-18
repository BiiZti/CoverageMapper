# 🗺️ 信号覆盖地图 (Signal Coverage Mapper)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-blue.svg)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)](https://html.spec.whatwg.org/)

一个基于高德地图的网络信号质量可视化工具，支持Excel数据导入、热力图显示和交互式分析。

## ✨ 功能特性

### 🖥️ 桌面GUI版本（推荐）
- 🚀 **一键启动**：无需手动配置，点击即用
- 🛠️ **内置服务器**：自动启动HTTP服务器，解决CORS问题
- 🎛️ **可视化控制**：实时状态监控，友好的图形界面
- 📁 **文件管理**：自动生成示例数据，支持文件选择
- 🌐 **自动打开**：启动后自动打开浏览器

### 🗺️ 地图分析功能
- 📁 **Excel数据导入**：支持 .xlsx/.xls 格式，自动解析信号监测数据
- 🗺️ **地图可视化**：基于高德地图，支持多种地图样式
- 🔥 **智能热力图**：自动聚合附近监测点，生成区域热力图
- 📍 **多样标记**：根据信号强度显示不同颜色和大小的标记
- 🎛️ **交互控制**：热力图开关、标记点开关、信号强度筛选
- 📊 **数据统计**：实时显示监测点概况和统计信息
- 🎨 **现代UI**：响应式设计，支持移动端访问

### 🧠 智能算法
- 🔄 **K-means聚类**：自动分组信号监测点
- 📈 **IDW插值预测**：预测未监测区域信号强度
- 🎯 **盲区检测**：使用凸包算法检测信号盲区边界
- 📊 **多维分析**：综合考虑信号强度、覆盖率、稳定性等指标

## 🚀 快速开始

### 方法1：GUI一键启动（强烈推荐！）
```bash
# Windows用户
双击 start_gui.bat

# 或Python命令
python signal_mapper_gui.py
```
**🎯 超简单使用**：
1. 启动GUI程序
2. 点击"🚀 一键启动完整服务"
3. 等待浏览器自动打开地图
4. 完成！

> **为什么需要HTTP服务器？** 现代浏览器的CORS安全策略要求从服务器加载文件，直接打开HTML文件无法访问本地Excel等资源。GUI程序内置了HTTP服务器，自动解决这个问题。

### 方法2：手动启动
```bash
# 1. 克隆项目
git clone https://github.com/yourusername/CoverageMapper.git
cd CoverageMapper

# 2. 安装依赖
pip install -r requirements.txt

# 3. 生成地图文件
python generate_amap_html.py

# 4. 启动HTTP服务器
python -m http.server 8888

# 5. 在浏览器中访问
http://localhost:8888/signal_coverage_map.html
```

## 📋 Excel数据格式

支持以下列格式的Excel文件：

| 列名 | 数据类型 | 示例 | 说明 |
|------|----------|------|------|
| 位置描述 | 文本 | 南通市崇川区南大街 | 监测点描述 |
| 详细地址 | 文本 | 江苏省南通市崇川区南大街128号 | 完整地址 |
| 网络类型 | 文本 | 5G/4G/3G | 网络制式 |
| 信号强度 | 数字 | 1-10 | 信号评分(1最差,10最好) |
| 上报时间 | 日期 | 2024-01-15 10:30 | 数据采集时间 |
| 上报人 | 文本 | 张三 | 数据采集人员 |
| 备注 | 文本 | 地下商场信号较弱 | 补充说明 |

## 🎯 使用方法

### 导入数据
1. 点击"加载数据"按钮选择Excel文件
2. 或点击"使用示例数据"查看演示效果

### 查看可视化
- **标记点**：不同颜色和大小表示信号强度
  - 🔴 红色大标记：严重盲区 (1-2分)
  - 🔴 红色小标记：信号较差 (3-4分)
  - 🔵 蓝色小标记：信号一般 (5-6分)
  - 🔵 蓝色大标记：信号良好 (7-10分)

- **热力图**：区域信号质量分布
  - 🔵 蓝色区域：信号优秀
  - 🟢 绿色区域：信号良好
  - 🟡 黄色区域：信号一般
  - 🟠 橙色区域：信号较差
  - 🔴 红色区域：信号盲区

### 交互控制
- **热力图开关**：控制热力图显示/隐藏
- **标记点开关**：控制标记点显示/隐藏
- **信号强度筛选**：只显示指定强度以下的监测点

## 🛠️ 技术架构

- **前端框架**：原生JavaScript (ES6+)
- **地图服务**：高德地图 Web API 2.0
- **数据处理**：XLSX.js (Excel解析)
- **UI框架**：原生CSS3 + Flexbox
- **图表可视化**：高德地图热力图插件

## 📱 浏览器支持

- ✅ Chrome 60+
- ✅ Firefox 60+
- ✅ Safari 12+
- ✅ Edge 79+
- ✅ 移动端浏览器

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源协议。

## 🙏 致谢

- [高德地图](https://lbs.amap.com/) - 提供地图服务和API
- [XLSX.js](https://github.com/SheetJS/sheetjs) - Excel文件解析
- [南通市](https://www.nantong.gov.cn/) - 示例数据来源

## 📞 联系方式

- 项目Issues: [GitHub Issues](https://github.com/yourusername/CoverageMapper/issues)
- 作者邮箱: your.email@example.com

---

⭐ 如果这个项目对你有帮助，请给个Star支持一下！ 
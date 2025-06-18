# 🔐 安全配置指南

## 📋 快速安全配置

本项目需要配置高德地图API密钥才能正常使用。请按照以下步骤进行安全配置。

## 🗝️ API密钥配置

### 步骤1：申请API密钥

1. 访问 [高德地图开放平台](https://developer.amap.com/)
2. 注册账号并登录
3. 在控制台创建新应用
4. 添加Key，选择"Web服务API"和"Web端(JS API)"
5. 记录生成的API密钥

### 步骤2：配置密钥

**方式一：配置文件方式（推荐）**

1. 编辑 `config_template.py` 文件
2. 替换API密钥：
```python
# 高德地图API配置
AMAP_WEB_API_KEY = "your_web_api_key_here"  # 替换为你的Web服务API密钥
AMAP_JS_API_KEY = "your_js_api_key_here"    # 替换为你的JavaScript API密钥
```

**方式二：环境变量方式**

设置环境变量：
```bash
# Windows
set AMAP_WEB_API_KEY=your_web_api_key
set AMAP_JS_API_KEY=your_js_api_key

# Linux/Mac
export AMAP_WEB_API_KEY="your_web_api_key"
export AMAP_JS_API_KEY="your_js_api_key"
```

### 步骤3：验证配置

运行程序，如果看到地图正常显示，说明配置成功。

## 🛡️ 安全注意事项

### API密钥安全
- ⚠️ **不要**将真实API密钥提交到GitHub等代码仓库
- ⚠️ **不要**在公开场所分享你的API密钥
- ✅ **建议**定期更换API密钥
- ✅ **建议**为API密钥设置使用限额

### 数据安全
- ✅ 上传的Excel文件仅在本地处理，不会上传到服务器
- ✅ 生成的地图文件保存在本地
- ✅ 程序不会收集或传输用户个人信息

### 网络安全
- ✅ HTTP服务器仅绑定本地地址(localhost)
- ✅ 不会暴露到外网，保证本地使用安全
- ✅ 所有网络请求均通过HTTPS加密

## 🔧 故障排除

### API密钥相关问题

**问题1：地图无法显示**
- 检查API密钥是否正确配置
- 确认密钥是否有效且未过期
- 检查网络连接是否正常

**问题2：提示"请配置API密钥"**
- 确认已正确编辑配置文件
- 或确认环境变量已正确设置
- 重启程序使配置生效

**问题3：API调用失败**
- 检查API密钥是否有相应权限
- 确认账户是否有足够的API调用额度
- 检查密钥是否绑定了正确的应用

### 配置验证

可以通过以下方式验证配置：

1. **检查配置文件**：
```bash
python -c "from config_template import AMAP_WEB_API_KEY; print('API密钥配置正常' if 'your_' not in AMAP_WEB_API_KEY else '请配置真实API密钥')"
```

2. **运行程序测试**：
   - 启动程序
   - 点击"一键启动完整服务"
   - 查看是否能正常显示地图

## 📞 技术支持

### 获取帮助
- **配置问题**：查看程序的"帮助文档"选项卡
- **日志信息**：查看 `signal_mapper.log` 文件
- **诊断工具**：使用程序的"系统检查"功能

### 常用API密钥服务商
- **高德地图**：https://developer.amap.com/ （推荐，免费额度充足）
- **百度地图**：https://lbsyun.baidu.com/ （需要代码修改支持）
- **腾讯地图**：https://lbs.qq.com/ （需要代码修改支持）

---

⚠️ **重要提醒**：请妥善保管你的API密钥，避免泄露和滥用！ 
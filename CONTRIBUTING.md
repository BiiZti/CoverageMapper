# 🤝 贡献指南 (Contributing Guide)

感谢您对 Signal Coverage Mapper 项目的贡献兴趣！我们欢迎各种形式的贡献，包括代码、文档、测试和反馈。

## 📋 贡献前必读

### 🔖 贡献者授权协议 (CLA)
**⚠️ 重要：在提交任何贡献之前，您必须同意我们的[贡献者授权协议](./CLA.md)。**

首次贡献时，请在您的Pull Request中包含以下声明：
```
我已阅读并同意贡献者授权协议(CLA)，确认我有权授权此贡献。
I have read and agree to the Contributor License Agreement (CLA), and confirm that I have the right to license this contribution.
```

## 🚀 快速开始

### 1. 设置开发环境
```bash
# 克隆项目
git clone https://github.com/yourusername/CoverageMapper.git
cd CoverageMapper

# 安装依赖
pip install -r requirements.txt

# 测试安装
python signal_mapper_gui.py
```

### 2. 创建功能分支
```bash
git checkout -b feature/amazing-feature
```

### 3. 进行更改
- 遵循代码风格指南
- 添加必要的测试
- 更新相关文档

### 4. 提交更改
```bash
git add .
git commit -m "Add some amazing feature"
git push origin feature/amazing-feature
```

### 5. 创建Pull Request
- 提供清晰的PR描述
- 确认已同意CLA协议
- 等待代码审查

## 📝 贡献类型

### 🐛 Bug报告
创建Issue时请包含：
- 操作系统和Python版本
- 详细的复现步骤
- 期望行为 vs 实际行为
- 错误日志（如有）
- 系统诊断信息

**模板：**
```markdown
**环境信息**
- OS: Windows 10
- Python: 3.9.0
- 项目版本: v2.0

**Bug描述**
清晰简洁的Bug描述

**复现步骤**
1. 执行 '...'
2. 点击 '....'
3. 发现错误

**期望行为**
应该发生什么

**实际行为**
实际发生了什么

**错误日志**
```
如果适用，请粘贴错误日志
```

**系统诊断**
运行"系统检查"的输出结果
```

### ✨ 功能请求
创建Issue时请说明：
- 功能的详细描述
- 使用场景和用户价值
- 可能的实现方案
- 是否愿意协助开发

### 🔧 代码贡献
我们欢迎以下类型的代码贡献：
- 新功能开发
- Bug修复
- 性能优化
- 代码重构
- 测试用例添加

### 📚 文档贡献
文档改进包括：
- API文档完善
- 使用教程更新
- 技术文档补充
- 翻译工作
- README优化

## 🎯 代码规范

### Python代码风格
- 遵循PEP 8标准
- 使用有意义的变量和函数名
- 添加适当的注释和文档字符串
- 保持函数简洁，单一职责

**示例：**
```python
def calculate_signal_strength(latitude: float, longitude: float) -> float:
    """
    计算指定位置的信号强度
    
    Args:
        latitude: 纬度
        longitude: 经度
        
    Returns:
        信号强度值 (1-10)
        
    Raises:
        ValueError: 当坐标无效时
    """
    if not (-90 <= latitude <= 90):
        raise ValueError("Invalid latitude")
    
    # 计算逻辑
    return signal_value
```

### GUI代码规范
- 使用清晰的组件命名
- 保持界面逻辑与业务逻辑分离
- 添加适当的错误处理
- 提供用户友好的反馈

### JavaScript/HTML规范
- 使用现代ES6+语法
- 保持代码模块化
- 添加适当的注释
- 确保跨浏览器兼容性

## 🧪 测试指南

### 运行测试
```bash
# 运行所有测试
python -m pytest

# 运行特定测试
python -m pytest tests/test_signal_analysis.py

# 生成覆盖率报告
python -m pytest --cov=signal_mapper
```

### 编写测试
- 为新功能添加单元测试
- 确保测试覆盖率 >= 80%
- 使用有意义的测试名称
- 包含正常和异常情况测试

**测试示例：**
```python
import pytest
from signal_mapper import SignalAnalyzer

class TestSignalAnalyzer:
    def test_analyze_signal_valid_data(self):
        """测试有效数据的信号分析"""
        analyzer = SignalAnalyzer()
        data = [{'signal': 8, 'position': [118.1, 32.0]}]
        result = analyzer.analyze(data)
        assert result['average_signal'] == 8
        
    def test_analyze_signal_empty_data(self):
        """测试空数据的处理"""
        analyzer = SignalAnalyzer()
        with pytest.raises(ValueError):
            analyzer.analyze([])
```

## 📋 Pull Request 流程

### PR检查清单
在提交PR前，请确认：
- [ ] 已同意CLA协议
- [ ] 代码通过所有测试
- [ ] 遵循代码风格指南
- [ ] 添加或更新了相关测试
- [ ] 更新了相关文档
- [ ] PR描述清晰详细
- [ ] 链接到相关Issues

### PR模板
```markdown
## 变更描述
简洁描述本次PR的主要变更

## 变更类型
- [ ] Bug修复
- [ ] 新功能
- [ ] 代码重构
- [ ] 文档更新
- [ ] 性能优化

## 测试
- [ ] 添加了新的测试用例
- [ ] 所有测试通过
- [ ] 手动测试通过

## CLA确认
- [ ] 我已阅读并同意贡献者授权协议(CLA)

## 相关Issue
Closes #(issue_number)

## 截图（如适用）
添加相关截图

## 其他说明
任何其他需要说明的信息
```

### 代码审查流程
1. **自动检查**：CI/CD自动运行测试和代码检查
2. **人工审查**：维护者进行代码审查
3. **讨论修改**：根据反馈进行必要修改
4. **合并代码**：审查通过后合并到主分支

## 🏆 贡献者认可

### 贡献者榜
我们在项目中维护贡献者列表，感谢每一位贡献者的努力。

### 贡献统计
- 代码提交数量
- Issue处理数量
- 文档改进次数
- 社区帮助积极性

## 📞 获取帮助

### 讨论渠道
- **GitHub Issues**: 报告问题和请求功能
- **GitHub Discussions**: 技术讨论和问答
- **项目邮箱**: [project@example.com]

### 新手指导
如果您是开源项目新手：
1. 从标有"good first issue"的简单问题开始
2. 阅读项目文档和代码
3. 不要害怕提问
4. 积极参与讨论

## 🚨 重要提醒

### 安全问题
如发现安全漏洞，请：
- **不要**在公开Issue中报告
- 发送邮件至安全团队：security@example.com
- 提供详细的漏洞信息
- 等待我们的回复和处理

### 行为准则
我们坚持友好、包容的社区环境：
- 尊重不同观点和经验
- 优雅地接受建设性批评
- 专注于对社区最有利的事情
- 对其他社区成员表现出同理心

---

**再次感谢您的贡献！每一个贡献都让项目变得更好。**

*如有任何疑问，随时通过Issue或邮件联系我们。* 
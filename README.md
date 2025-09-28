# ComfyUI-Xktools

一个专为ComfyUI设计的中文提示词翻译插件，使用百度翻译API将中文提示词自动翻译为英文，让中文用户能够更方便地使用ComfyUI进行AI图像生成。

## ✨ 主要功能

- 🌏 **中文翻译**：自动将中文提示词翻译为英文
- 🎯 **CLIP集成**：翻译后直接进行CLIP文本编码
- 💾 **配置保存**：支持保存百度翻译API配置
- 🔧 **灵活控制**：可选择是否启用自动翻译
- 📱 **节点内显示**：翻译结果直接在节点内显示

## 🚀 安装方法

### 方法一：通过ComfyUI Manager安装（推荐）
1. 在ComfyUI中打开Manager
2. 搜索"Xktools"
3. 点击安装

### 方法二：手动安装
1. 进入ComfyUI的`custom_nodes`目录
2. 克隆本仓库：
   ```bash
   git clone https://github.com/oskey/ComfyUI-Xktools.git
   ```
3. 安装依赖：
   ```bash
   cd ComfyUI-Xktools
   pip install -r requirements.txt
   ```
4. 重启ComfyUI

## 📋 依赖安装

```bash
pip install requests
```

## 🔑 百度翻译API申请教程

1. 访问 [百度翻译开放平台](https://fanyi-api.baidu.com/)
2. 注册并登录百度账号
3. 进入"管理控制台"
4. 点击"开通服务"，选择"通用翻译API"
5. 创建应用，获取APP ID和密钥
6. 在节点中填入APP ID和密钥

> 💡 **提示**：百度翻译API每月有免费额度，对于个人使用完全够用。

## 📖 使用说明

### 中文CLIP文本编码器

这是插件的核心节点，提供以下功能：

**输入参数：**
- `clip`：CLIP模型（必需）
- `chinese_text`：中文提示词（必需）
- `auto_translate`：是否自动翻译（布尔值）
- `app_id`：百度翻译API的APP ID
- `app_key`：百度翻译API的密钥
- `save_config`：是否保存API配置（可选）

**输出：**
- `条件`：CLIP编码后的条件
- `翻译结果`：翻译后的英文文本

**特点：**
- 翻译结果直接在节点内显示
- 支持配置保存，下次使用时自动加载
- 翻译失败时自动使用原文
- 可选择关闭自动翻译功能

## 💡 使用示例

### 基本使用
1. 在ComfyUI中添加"XKT 自动翻译英文CLIP文本编码器"节点
2. 连接CLIP模型到节点
3. 在`chinese_text`字段输入中文提示词，如："一个美丽的女孩，长发飘逸，微笑着看向镜头"
4. 填入百度翻译API的APP ID和密钥
5. 启用`auto_translate`
6. 运行工作流，翻译结果会直接显示在节点内

## ❓ 常见问题

**Q: 翻译失败怎么办？**
A: 请检查网络连接和API配置是否正确。翻译失败时会自动使用原文进行编码。

**Q: 可以不使用翻译功能吗？**
A: 可以，将`auto_translate`设置为False即可直接使用原文进行编码。

**Q: API配置会保存吗？**
A: 启用`save_config`选项后，API配置会自动保存，下次使用时无需重新输入。

## 🛠️ 技术支持

如果遇到问题，请：
1. 检查ComfyUI控制台的错误信息
2. 确认百度翻译API配置正确
3. 在GitHub Issues中提交问题

## 📝 更新日志

### v1.0.0 (2024-01-XX)
- 🎉 初始版本发布
- ✨ 支持中文到英文的自动翻译
- 🔧 集成CLIP文本编码功能
- 💾 支持API配置保存
- 📱 节点内翻译结果显示

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🤝 贡献

欢迎提交Pull Request和Issue！

---

**作者**: oskey  
**项目地址**: https://github.com/oskey/ComfyUI-Xktools
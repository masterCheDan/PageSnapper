# PageSnapper

**PageSnapper** 是一款简单高效的截图工具，旨在帮助用户通过指定区域进行截图并进行预览、保存等操作。支持按需截图、自动截图和截图命名设置，提供简洁的用户界面。

> ✨ 项目初期的大多数代码都是由 [ChatGPT](https://openai.com/chatgpt) (GPT-4o)生成的.

## 📦 功能

- **指定区域截图** 可以由鼠标框选截图区域
- **精准的区域划分** 像素级精确定位
- **自定义截图文件名称** 以及截图文件统一编号，用户可自定义起始编号
- **最近截图预览** 附带简洁的GUI界面
- **手动和自动截图两种模式**
- **连续截图** 交互十分友好
- **热键支持** 在软件内可以自定义热切换
- **明了的交互界面** 所有设置和自定义功能都有

## 🖥️ 适用场景

本工具适用于：

- 具有DRM保护的在线数字内容
- 将网页上的小说、漫画等保存到本地
- 持续截图监控屏幕上的特定区域

## 🛠️ 技术栈

使用前确保已安装如下内容：

- Python 3.10+
- Tkinter (for GUI)
- PIL / Pillow (for image handling)
- PyAutoGUI (for screen capturing)

## 🚀 安装使用

```bash
git clone git@github.com:masterCheDan/PageSnapper.git
cd PageSnapper
python screenshot.py
```

## 🧠 注意事项

- 启动时可以自行通过鼠标点选设置截图区域
- 所有主要操作都可以通过热键和按钮点击两种方式完成
- 可自定义的设置项都有GUI支持
- 持续截图将会一直持续到停止指令或是程序被强制关闭

## 📄 协议

本项目采用 **MIT 协议** — 查看 [LICENSE](LICENSE) 文件了解详情.

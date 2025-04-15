🧾 AutoVoucherVerifier

A visual-AI-powered tool that automatically verifies sales vouchers using the Qwen-VL-Plus multimodal model.

> 中文项目说明见下方 👇

---

🔍 What is this?

AutoVoucherVerifier** lets you define what a “qualified voucher” is using a natural language prompt, and lets an AI vision model decide whether each scanned voucher image passes or not. The model will then automatically click **“通过” (Approve)** or **“驳回” (Reject)** based on the result.

---

💡 Features

- 🧠 Uses Qwen-VL-Plus (Vision Language Model) for understanding voucher content
- 🖱 Auto-clicks "通过"/"驳回" using image template matching (no DOM, no OCR!)
- ⚙️ User-defined prompt for controlling judgment logic
- 🖼 Built-in image loader to prepare image list
- 🎯 One-click .exe launcher for non-tech users

---

📁 Project Structure

AutoVoucherVerifier/ ├── tubiao/ # 图标匹配图片（通过、驳回、关闭、查看） ├── 图片加载器.py # GUI 文件选择器，用 PyInstaller 打包为 .exe ├── 自动审核.py # 调用 Qwen-VL-Plus 审核图片，并执行点击动作


---

⚙️ How to Use

✅ Step 1: 打包 GUI（只需一次）

```bash
cd D:\AutoVoucherVerifier ##填你存放这个文件的路径
pyinstaller --noconsole --onefile "图片加载器.py"

✅ Step 2: 启动项目
先双击打开打包好的 图片加载器.exe → 会弹出文件夹选择窗口

选择存放销售凭证的文件夹（里面必须是图片，如 .jpg, .png）

然后运行：

bash:
python 自动审核.py

该脚本会：

使用 Qwen-VL-Plus 模型读取图片内容

通过 prompt 判断是否“合格”

合格（模型返回 1）→ 点击“通过”按钮图标

不合格（模型返回 0）→ 点击“驳回”按钮图标

所有按钮点击行为基于 /tubiao/*.png 图标匹配，请确保图标完整

合格的和不合格的图片都会被放入分类文件夹

✨ Prompt 自定义示例
你可以在 自动审核.py 中配置 prompt，自行定义什么是合格的销售凭证：
python：
prompt = "如果这是正规销售凭证并带有金额、印章和签名，返回1，否则返回0"
任何语言、任何条件，模型都能理解！

📦 Requirements
Python >= 3.10
pyautogui
opencv-python
requests
transformers（视具体模型封装而定）
已部署或远程访问的 Qwen-VL-Plus API

🔒 图标说明（tubiao 文件夹）
图标名 | 用途
chakan.png | 查看按钮
tongguo.png | 通过按钮
bohui.png | 驳回按钮
guanbi.png | 关闭按钮

💬 中文总结
本项目是一个自动化视觉审核系统：
✅ 无需 OCR、无需手动检查
✅ 视觉模型识别内容后自主判断
✅ 模拟真实用户点击行为
✅ 批量处理销售凭证效率极高！

🧠 灵感来自
本人日常工作中的真实业务场景：
“让大模型看懂图片、判断它们合不合格，并像人一样操作系统”

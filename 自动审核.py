import cv2
import numpy as np
import pyautogui
import time
import base64
from io import BytesIO
from PIL import ImageGrab
from openai import OpenAI

# ====== 配置项 ======
API_KEY = "sk-xxx"  # 替换为你的 DashScope Key ##没有的话就去qwen官网获取
ICON_DIR = r"D:\tubiao"# 替换为你的 存放tubiao文件夹的位置
THRESHOLD = 0.80  # 模板匹配置信度

client = OpenAI(
    api_key=API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 审核提示
AUDIT_PROMPT = (
    "这是销售凭证截图，请判断是否合格，合格返回1，不合格返回0：\n"
    "必须包含商户名、日期、金额。\n"
    "只要看到店字就说明包含商户名，商户名这部分就合格了\n"
    "只要看到日期这两个字则日期就合格了\n"
    "缺项则为不合格。\n"
    "仅返回：1 或 0。"
)

# ====== 工具函数 ======

def screenshot_to_dataurl():
    img = ImageGrab.grab()
    buf = BytesIO()
    img.save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}"

def gpt_judge_image(image_dataurl):
    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": AUDIT_PROMPT},
            {"type": "image_url", "image_url": {"url": image_dataurl}}
        ]
    }]
    try:
        response = client.chat.completions.create(
            model="qwen-vl-plus",
            messages=messages
        )
        result = response.choices[0].message.content.strip()
        print(f"🧠 GPT判断结果：{result}")
        return result
    except Exception as e:
        print("❌ GPT出错：", e)
        return None

def match_and_click(img_name):
    full_path = f"{ICON_DIR}\\{img_name}"
    template = cv2.imread(full_path)
    if template is None:
        print(f"❌ 无法读取图标：{full_path}")
        return False

    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= THRESHOLD:
        h, w = template.shape[:2]
        center = (max_loc[0] + w//2, max_loc[1] + h//2)
        pyautogui.click(center)
        print(f"✅ 点击 {img_name} → {center}，置信度：{max_val:.2f}")
        return True
    else:
        print(f"⚠️ 匹配失败 {img_name}，置信度：{max_val:.2f}")
        return False

# ====== 主流程 ======

def audit_once():
    print("\n🔁 新一轮审核开始")

    # Step 1：点击“查看”
    if not match_and_click("chakan.png"):
        print("➡️ 未找到查看，跳过本轮")
        return

    time.sleep(2)

    # Step 2：截图并提交GPT审核
    data_url = screenshot_to_dataurl()
    result = gpt_judge_image(data_url)

    time.sleep(0.8)
    match_and_click("guanbi.png")

    time.sleep(0.8)
    if "1" in result:
        match_and_click("tongguo.png")
    elif "0" in result:
        match_and_click("bohui.png")
    else:
        print("❓ 无效审核结果，跳过本轮")

# ====== 主程序入口 ======

if __name__ == "__main__":
    print("🚀 自动审核系统启动")
    try:
        while True:
            audit_once()
            time.sleep(1.5)
    except KeyboardInterrupt:
        print("⛔ 手动中止")

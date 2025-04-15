import os
import shutil
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# === 配置 ===
IMAGE_DIR = r"C:"##输入你要审核的图片所在的文件夹路径
RESULT_DIR = os.path.join(IMAGE_DIR, "审核结果")
PASSED_DIR = os.path.join(RESULT_DIR, "通过")
REJECTED_DIR = os.path.join(RESULT_DIR, "驳回")

# 创建目标文件夹（如果不存在）
os.makedirs(PASSED_DIR, exist_ok=True)
os.makedirs(REJECTED_DIR, exist_ok=True)

# 审核结果记录
passed_images = []
rejected_images = []
current_index = 0

def load_images(directory):
    valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if os.path.splitext(f)[1].lower() in valid_extensions]

def view_image():
    global current_index, image_files
    if current_index >= len(image_files):
        messagebox.showinfo("提示", "没有图片可查看！")
        return
    top = tk.Toplevel(root)
    top.title("查看图片")

    top_frame = tk.Frame(top)
    top_frame.pack(fill="x")
    close_button = tk.Button(top_frame, text="×", command=top.destroy,
                             font=("Arial", 12), bg="red", fg="white")
    close_button.pack(side="right", padx=5, pady=5)

    try:
        img = Image.open(image_files[current_index])
    except Exception as e:
        messagebox.showerror("错误", f"加载图片失败：{e}")
        top.destroy()
        return
    photo = ImageTk.PhotoImage(img)
    img_label = tk.Label(top, image=photo)
    img_label.image = photo
    img_label.pack(padx=10, pady=10)

def process_image(result):
    global current_index, image_files
    if current_index < len(image_files):
        filepath = image_files[current_index]
        filename = os.path.basename(filepath)

        if result == "pass":
            passed_images.append(filename)
            shutil.copy(filepath, os.path.join(PASSED_DIR, filename))
        elif result == "reject":
            rejected_images.append(filename)
            shutil.copy(filepath, os.path.join(REJECTED_DIR, filename))

        current_index += 1
        if current_index < len(image_files):
            update_status()
        else:
            show_summary()

def update_status():
    global current_index, image_files
    status_label.config(
        text=f"当前图片 {current_index+1} / {len(image_files)}: {os.path.basename(image_files[current_index])}"
    )

def show_summary():
    summary_text = (
        f"审核完成！\n\n✅ 通过的图片:\n{chr(10).join(passed_images)}\n\n"
        f"❌ 驳回的图片:\n{chr(10).join(rejected_images)}"
    )
    messagebox.showinfo("审核结果", summary_text)
    root.destroy()

# === 主界面 ===
root = tk.Tk()
root.title("模拟公司审核后台")

image_files = load_images(IMAGE_DIR)
if not image_files:
    messagebox.showerror("错误", "指定文件夹中没有找到图片文件！")
    root.destroy()
    exit()

status_label = tk.Label(root, text="", font=("Arial", 12))
status_label.pack(pady=10)
update_status()

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

view_button = tk.Button(button_frame, text="查看", width=10, command=view_image)
view_button.grid(row=0, column=0, padx=5)

pass_button = tk.Button(button_frame, text="通过", width=10, command=lambda: process_image("pass"))
pass_button.grid(row=0, column=1, padx=5)

reject_button = tk.Button(button_frame, text="驳回", width=10, command=lambda: process_image("reject"))
reject_button.grid(row=0, column=2, padx=5)

root.mainloop()

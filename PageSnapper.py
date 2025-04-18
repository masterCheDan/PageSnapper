import os
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
import pyautogui


# === GUI 初始化必须最前面 ===
root = tk.Tk()

# === 初始化截图区域 ===
x1, y1, x2, y2 = 100, 100, 500, 400
width, height = x2 - x1, y2 - y1

# === 状态变量 ===
current_index = [0]
is_auto_capturing = tk.BooleanVar(value=False)
auto_capture_job = [None]
hotkeys = {
    "single_capture": "s",
    "start_auto": "a",
    "stop_auto": "d"
}

# === GUI 初始化 ===
root.title("PageSnapper")
root.geometry("640x580")

# === 用户输入变量 ===
save_path = tk.StringVar(value="screenshots")
filename_prefix = tk.StringVar(value="screenshot_")
start_index = tk.IntVar(value=0)
interval_var = tk.StringVar(value="2")

# === 功能函数 ===

def take_screenshot():
    global x1, y1, width, height
    if is_auto_capturing.get():
        pass  # 自动截图时允许执行
    else:
        if is_auto_capturing.get():
            return
    folder = save_path.get()
    if not os.path.isdir(folder):
        os.makedirs(folder)
    filename = f"{filename_prefix.get()}{current_index[0]}.png"
    filepath = os.path.join(folder, filename)
    screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
    screenshot.save(filepath)
    print(f"已截图，保存为 {filepath}")
    show_preview(filepath)
    current_index[0] += 1

def show_preview(image_path):
    try:
        with Image.open(image_path) as img:
            img.thumbnail((400, 300))
            img_tk = ImageTk.PhotoImage(img.copy())
        preview_label.config(image=img_tk, text="")
        preview_label.image = img_tk
    except Exception as e:
        print(f"预览图加载失败：{e}")
        preview_label.config(text="图片加载失败")

def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        save_path.set(folder)
        os.makedirs(folder, exist_ok=True)

def apply_start_index():
    current_index[0] = start_index.get()
    print(f"编号重置为：{current_index[0]}")

def select_capture_area():
    selector = tk.Toplevel()
    selector.attributes("-fullscreen", True)
    selector.attributes("-alpha", 0.3)
    selector.config(bg="black")
    selector.title("拖动选择截图区域")

    canvas = tk.Canvas(selector, cursor="cross", bg="gray", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    start = [0, 0]
    rect = [None]
    h_line = [None]
    v_line = [None]

    def on_mouse_down(event):
        start[0], start[1] = event.x, event.y
        rect[0] = canvas.create_rectangle(start[0], start[1], start[0], start[1], outline="red", width=2)
        h_line[0] = canvas.create_line(0, event.y, canvas.winfo_width(), event.y, fill="white", dash=(4, 2))
        v_line[0] = canvas.create_line(event.x, 0, event.x, canvas.winfo_height(), fill="white", dash=(4, 2))

    def on_mouse_move(event):
        if rect[0]:
            canvas.coords(rect[0], start[0], start[1], event.x, event.y)
        if h_line[0]:
            canvas.coords(h_line[0], 0, event.y, canvas.winfo_width(), event.y)
        if v_line[0]:
            canvas.coords(v_line[0], event.x, 0, event.x, canvas.winfo_height())

    def on_mouse_up(event):
        global x1, y1, x2, y2, width, height
        end_x, end_y = event.x, event.y
        x1, y1 = min(start[0], end_x), min(start[1], end_y)
        x2, y2 = max(start[0], end_x), max(start[1], end_y)
        width, height = x2 - x1, y2 - y1
        print(f"新截图区域：({x1}, {y1}) 到 ({x2}, {y2})")
        selector.destroy()

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_move)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

def start_auto_capture():
    try:
        interval = float(interval_var.get())
    except ValueError:
        print("请输入有效的数字作为间隔时间（单位：秒）")
        return
    is_auto_capturing.set(True)
    disable_controls()
    auto_loop(interval)

def auto_loop(interval):
    if not is_auto_capturing.get():
        return
    take_screenshot()
    auto_capture_job[0] = root.after(int(interval * 1000), lambda: auto_loop(interval))

def stop_auto_capture():
    is_auto_capturing.set(False)
    if auto_capture_job[0]:
        root.after_cancel(auto_capture_job[0])
        auto_capture_job[0] = None
    enable_controls()
    print("已停止连续截图")

def disable_controls():
    capture_button.config(state="disabled")
    select_button.config(state="disabled")
    apply_button.config(state="disabled")
    index_entry.config(state="disabled")
    path_entry.config(state="disabled")
    prefix_entry.config(state="disabled")
    interval_entry.config(state="disabled")

def enable_controls():
    capture_button.config(state="normal")
    select_button.config(state="normal")
    apply_button.config(state="normal")
    index_entry.config(state="normal")
    path_entry.config(state="normal")
    prefix_entry.config(state="normal")
    interval_entry.config(state="normal")

def configure_hotkeys():
    config_win = tk.Toplevel(root)
    config_win.title("快捷键设置")
    config_win.geometry("300x300")
    config_win.resizable(False, False)

    tk.Label(config_win, text="单次截图快捷键:").pack(pady=(10, 0))
    single_entry = tk.Entry(config_win)
    single_entry.insert(0, hotkeys["single_capture"])
    single_entry.pack()

    tk.Label(config_win, text="开始连续截图快捷键:").pack(pady=(10, 0))
    start_entry = tk.Entry(config_win)
    start_entry.insert(0, hotkeys["start_auto"])
    start_entry.pack()

    tk.Label(config_win, text="停止连续截图快捷键:").pack(pady=(10, 0))
    stop_entry = tk.Entry(config_win)
    stop_entry.insert(0, hotkeys["stop_auto"])
    stop_entry.pack()

    def save_and_close():
        hotkeys["single_capture"] = single_entry.get().strip().lower()
        hotkeys["start_auto"] = start_entry.get().strip().lower()
        hotkeys["stop_auto"] = stop_entry.get().strip().lower()
        bind_hotkeys()
        config_win.destroy()

    tk.Button(config_win, text="保存设置", command=save_and_close, bg="#4CAF50", fg="white").pack(pady=15)

def bind_hotkeys():
    root.unbind_all(f"<{hotkeys['single_capture']}>")
    root.unbind_all(f"<{hotkeys['start_auto']}>")
    root.unbind_all(f"<{hotkeys['stop_auto']}>")

    root.bind_all(f"<{hotkeys['single_capture']}>", lambda e: take_screenshot() if not is_auto_capturing.get() else None)
    root.bind_all(f"<{hotkeys['start_auto']}>", lambda e: start_auto_capture())
    root.bind_all(f"<{hotkeys['stop_auto']}>", lambda e: stop_auto_capture())

# === 菜单 ===
menubar = tk.Menu(root)
setting_menu = tk.Menu(menubar, tearoff=0)
setting_menu.add_command(label="设置快捷键", command=configure_hotkeys)
menubar.add_cascade(label="设置", menu=setting_menu)
root.config(menu=menubar)

# === GUI 元素 ===

frame = tk.Frame(root)
frame.pack(pady=5)
tk.Label(frame, text="保存路径:").pack(side=tk.LEFT)
path_entry = tk.Entry(frame, textvariable=save_path, width=40)
path_entry.pack(side=tk.LEFT, padx=5)
browse_button = tk.Button(frame, text="选择文件夹", command=choose_folder)
browse_button.pack(side=tk.LEFT)

prefix_frame = tk.Frame(root)
prefix_frame.pack(pady=5)
tk.Label(prefix_frame, text="文件名前缀:").pack(side=tk.LEFT)
prefix_entry = tk.Entry(prefix_frame, textvariable=filename_prefix, width=20)
prefix_entry.pack(side=tk.LEFT, padx=5)

index_frame = tk.Frame(root)
index_frame.pack(pady=5)
tk.Label(index_frame, text="开始编号:").pack(side=tk.LEFT)
index_entry = tk.Entry(index_frame, textvariable=start_index, width=6)
index_entry.pack(side=tk.LEFT, padx=5)
apply_button = tk.Button(index_frame, text="应用编号", command=apply_start_index)
apply_button.pack(side=tk.LEFT)

interval_frame = tk.Frame(root)
interval_frame.pack(pady=5)
tk.Label(interval_frame, text="连续截图间隔(秒):").pack(side=tk.LEFT)
interval_entry = tk.Entry(interval_frame, textvariable=interval_var, width=5)
interval_entry.pack(side=tk.LEFT)

select_button = tk.Button(root, text="选择截图区域", command=select_capture_area, bg="#2196F3", fg="white")
select_button.pack(pady=5)

capture_button = tk.Button(root, text="截图", command=take_screenshot, bg="#4CAF50", fg="white", font=("Arial", 12))
capture_button.pack(pady=5)

auto_btn_frame = tk.Frame(root)
auto_btn_frame.pack(pady=5)
start_auto_btn = tk.Button(auto_btn_frame, text="开始连续截图", command=start_auto_capture, bg="#FF9800", fg="white")
start_auto_btn.pack(side=tk.LEFT, padx=10)
stop_auto_btn = tk.Button(auto_btn_frame, text="停止连续截图", command=stop_auto_capture, bg="#f44336", fg="white")
stop_auto_btn.pack(side=tk.LEFT, padx=10)

preview_label = tk.Label(root, text="截图预览将在此显示", bd=2, relief=tk.SUNKEN, width=1920, height=1080)
preview_label.pack(pady=10)

# 初次绑定快捷键
bind_hotkeys()

# 启动主程序
root.mainloop()

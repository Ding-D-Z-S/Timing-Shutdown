import tkinter as tk
from tkinter import ttk
import time
import math
import os
import sys

# 更新时钟显示
def update_clock():
    current_time = time.localtime()
    hour = current_time.tm_hour
    minute = current_time.tm_min
    second = current_time.tm_sec

    sec_angle = -6 * second + 90
    min_angle = -6 * minute + 90
    hour_angle = -30 * (hour % 12) - 0.5 * minute + 90

    canvas.delete("clock_hands")
    draw_hand(hour_angle, 40, "black", 8, 20)
    draw_hand(min_angle, 60, "blue", 5, 30)
    draw_hand(sec_angle, 70, "red", 2, 40)

    current_time_label.config(text=time.strftime("%H:%M:%S", current_time))

    root.after(1000, update_clock)

# 绘制时钟指针
def draw_hand(angle, length, color, width, offset):
    x = center_x + length * math.cos(math.radians(angle))
    y = center_y - length * math.sin(math.radians(angle))
    canvas.create_line(center_x, center_y, x, y, fill=color, width=width, tags="clock_hands")

root = tk.Tk()
root.title("定时关机程序@叮当在上")
root.geometry("1000x400")  # 设置窗口大小为600x400像素
root.resizable(width=False, height=False)  # 禁止调整窗口大小

canvas_width = 200
canvas_height = 200
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack(side=tk.TOP, padx=10, pady=10)

center_x = canvas_width // 2
center_y = canvas_height // 2

clock_radius = 80
canvas.create_oval(center_x - clock_radius, center_y - clock_radius,
                   center_x + clock_radius, center_y + clock_radius, outline="black", width=2)

# 绘制时钟刻度和标注
for i in range(12):
    angle = -30 * i + 90
    x1 = center_x + (clock_radius - 10) * math.cos(math.radians(angle))
    y1 = center_y - (clock_radius - 10) * math.sin(math.radians(angle))
    x2 = center_x + clock_radius * math.cos(math.radians(angle))
    y2 = center_y - clock_radius * math.sin(math.radians(angle))
    canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
    x_text = center_x + (clock_radius - 30) * math.cos(math.radians(angle))
    y_text = center_y - (clock_radius - 30) * math.sin(math.radians(angle))
    canvas.create_text(x_text, y_text, text=str(i+1), font=("Helvetica", 12, "bold"))

current_time_label = tk.Label(root, text="", font=("Helvetica", 16))
current_time_label.pack()

shutdown_frame = tk.Frame(root)
shutdown_frame.pack(side=tk.LEFT, padx=10)

# 创建关机日期的标签和下拉框
shutdown_date_label = tk.Label(shutdown_frame, text="关机日期：", font=("Helvetica", 12))
shutdown_date_label.grid(row=0, column=0, padx=5, pady=5)

shutdown_year_var = tk.StringVar()
shutdown_year_combobox = ttk.Combobox(shutdown_frame, textvariable=shutdown_year_var, values=[str(i) for i in range(time.localtime().tm_year, time.localtime().tm_year + 11)], state="readonly", font=("Helvetica", 12))
shutdown_year_combobox.grid(row=0, column=1)

shutdown_month_var = tk.StringVar()
shutdown_month_combobox = ttk.Combobox(shutdown_frame, textvariable=shutdown_month_var, values=[str(i).zfill(2) for i in range(1, 13)], state="readonly", font=("Helvetica", 12))
shutdown_month_combobox.grid(row=0, column=2)

shutdown_day_var = tk.StringVar()
shutdown_day_combobox = ttk.Combobox(shutdown_frame, textvariable=shutdown_day_var, values=[str(i).zfill(2) for i in range(1, 32)], state="readonly", font=("Helvetica", 12))
shutdown_day_combobox.grid(row=0, column=3)

# 创建关机时间的标签和下拉框
shutdown_time_label = tk.Label(shutdown_frame, text="关机时间：", font=("Helvetica", 12))
shutdown_time_label.grid(row=1, column=0, padx=5, pady=5)

shutdown_hour_var = tk.StringVar()
shutdown_hour_combobox = ttk.Combobox(shutdown_frame, textvariable=shutdown_hour_var, values=[str(i).zfill(2) for i in range(24)], state="readonly", font=("Helvetica", 12))
shutdown_hour_combobox.grid(row=1, column=1)

shutdown_minute_var = tk.StringVar()
shutdown_minute_combobox = ttk.Combobox(shutdown_frame, textvariable=shutdown_minute_var, values=[str(i).zfill(2) for i in range(60)], state="readonly", font=("Helvetica", 12))
shutdown_minute_combobox.grid(row=1, column=2)

shutdown_second_var = tk.StringVar()
shutdown_second_combobox = ttk.Combobox(shutdown_frame, textvariable=shutdown_second_var, values=[str(i).zfill(2) for i in range(60)], state="readonly", font=("Helvetica", 12))
shutdown_second_combobox.grid(row=1, column=3)

# 设置关机时间函数
def set_shutdown_time():
    shutdown_date_str = f"{shutdown_year_var.get()}-{shutdown_month_var.get()}-{shutdown_day_var.get()}"
    shutdown_time_str = f"{shutdown_hour_var.get()}:{shutdown_minute_var.get()}:{shutdown_second_var.get()}"
    shutdown_datetime_str = shutdown_date_str + " " + shutdown_time_str

    try:
        shutdown_time = time.strptime(shutdown_datetime_str, "%Y-%m-%d %H:%M:%S")
        shutdown_timestamp = time.mktime(shutdown_time)
        current_timestamp = time.time()

        if shutdown_timestamp <= current_timestamp:
            output_text.insert(tk.END, "指定的时间早于当前时间，无法关机。\n")
        else:
            wait_time = int(shutdown_timestamp - current_timestamp)
            output_text.insert(tk.END, f"计算机将在 {shutdown_datetime_str} 关机。\n")
            root.after(wait_time * 1000, os.system, "shutdown /s /t 0")
    except ValueError:
        output_text.insert(tk.END, "输入的时间格式不正确，请重新输入。\n")

# 取消关机函数
def cancel_shutdown():
    os.system("shutdown /a")
    shutdown_year_var.set("")
    shutdown_month_var.set("")
    shutdown_day_var.set("")
    shutdown_hour_var.set("")
    shutdown_minute_var.set("")
    shutdown_second_var.set("")
    output_text.insert(tk.END, "已取消关机设置。\n")

    # 终止当前正在执行的关机操作
    os.system("taskkill /F /IM shutdown.exe")

    # 关闭整个应用程序，闪退
    root.destroy()

# 创建设置关机时间的按钮和取消关机设置的按钮
shutdown_button = tk.Button(shutdown_frame, text="确认关机设置", command=set_shutdown_time, font=("Helvetica", 14))
shutdown_button.grid(row=2, column=0, columnspan=4, pady=10)

cancel_button = tk.Button(shutdown_frame, text="取消关机设置", command=cancel_shutdown, font=("Helvetica", 14))
cancel_button.grid(row=2, column=3, columnspan=4, pady=10)
'''row: 表示组件在网格布局中的行数。行号从0开始，表示在第几行放置组件。
   column: 表示组件在网格布局中的列数。列号从0开始，表示在第几列放置组件。
   columnspan: 表示组件横向跨越的列数。默认为1，即组件只占据一个单元格。如果设置为2，组件将横向跨越两个单元格，依此类推。
   pady: 表示在组件的顶部和底部添加的外部垂直填充（padding）。
         它是以像素为单位的整数值，用于控制组件在垂直方向上与其他组件或边界之间的间距。

 在上述代码中，cancel_button.grid(row=3, column=0, columnspan=4, pady=10)
 这一行代码将取消按钮放置在网格布局中的第3行第0列，并设置横向跨越4列，垂直方向上的外部填充为10像素。'''


# 创建输出文本框和滚动条
output_text = tk.Text(root, width=30, height=10, wrap=tk.WORD)
output_text.pack(side=tk.RIGHT, padx=10, pady=10)


scrollbar = tk.Scrollbar(root, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text.config(yscrollcommand=scrollbar.set)
# 插入提示信息到输出栏
output_text.insert(tk.END, "欢迎使用叮当在上的电脑定时关机程序程序！\n")
output_text.insert(tk.END, "*****************************\n")
output_text.insert(tk.END, "1.请在左侧选择关机日期和时间，并点击确认关机设置按钮。\n")
output_text.insert(tk.END, "2.如果想取消关机设置，请点击取消关机设置按钮。\n")
output_text.insert(tk.END, "3.请注意，关机日期和时间不能早于当前日期和时间。\n")
output_text.insert(tk.END, "*****************************\n")

# 更新时钟
update_clock()

root.mainloop()

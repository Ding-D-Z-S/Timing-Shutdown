import tkinter as tk
from tkinter import ttk
import time
import math
import os
import sys

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

def draw_hand(angle, length, color, width, offset):
    x = center_x + length * math.cos(math.radians(angle))
    y = center_y - length * math.sin(math.radians(angle))
    canvas.create_line(center_x, center_y, x, y, fill=color, width=width, tags="clock_hands")

root = tk.Tk()
root.title("模拟时钟")

canvas_width = 200
canvas_height = 200
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack(side=tk.TOP, padx=10, pady=10)

center_x = canvas_width // 2
center_y = canvas_height // 2

clock_radius = 80
canvas.create_oval(center_x - clock_radius, center_y - clock_radius,
                   center_x + clock_radius, center_y + clock_radius, outline="black", width=2)

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

shutdown_button = tk.Button(shutdown_frame, text="设置关机时间", command=set_shutdown_time, font=("Helvetica", 14))
shutdown_button.grid(row=2, column=0, columnspan=4, pady=10)

output_text = tk.Text(root, width=30, height=10, wrap=tk.WORD)
output_text.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(root, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text.config(yscrollcommand=scrollbar.set)

update_clock()

root.mainloop()

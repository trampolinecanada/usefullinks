import tkinter as tk
from tkinter import ttk
from math import trunc
import sys

default_num_frames = 60

def mode_num():
	#0: TRI Times
	#1: TRI Frames
	#2: TRS Times
	#3: TRS Frames
	return calc_type.get()+event_type.get()*2

def change_calc_type(*args):
	mode = mode_num()
	if mode == 0 or mode == 2:
		num_fps.grid_remove()
		fps_label.grid_remove()
	else:
		num_fps.grid()
		fps_label.grid()
	if mode == 0:
		TRI_time_frame.grid()
		TRI_frames_frame.grid_remove()
		TRS_frames_frame.grid_remove()
		TRS_time_frame.grid_remove()
	elif mode == 1:
		TRI_frames_frame.grid()
		TRI_time_frame.grid_remove()
		TRS_frames_frame.grid_remove()
		TRS_time_frame.grid_remove()
	elif mode == 2:
		TRS_time_frame.grid()
		TRI_frames_frame.grid_remove()
		TRI_time_frame.grid_remove()
		TRS_frames_frame.grid_remove()
	elif mode == 3:
		TRS_frames_frame.grid()
		TRI_frames_frame.grid_remove()
		TRI_time_frame.grid_remove()
		TRS_time_frame.grid_remove()
	calculate_score()

def calculate_time_times(t1,t2):
	if t1 == '' or t1 == '.':
		t1 = 0
	if t2 == '' or t2 == '.':
		t2 = 0
	return float(t2)-float(t1)

def calculate_time_fps(frame_num,fps):
	if frame_num == '':
		frame_num = 0
	return float(frame_num)/float(fps)

def calculate_score(*args):
	total = 0
	num_skills_complete = 10
	mode = mode_num()
	if mode == 1:
		TRI_frames_frame.grid()
	elif mode == 3:
		TRS_frames_frame.grid()
	fps_error_indicator.grid_remove()
	fps = num_fps.get()
	if (fps == '' or int(fps) == 0) and (mode == 1 or mode == 3):
		fps_error_indicator.grid()
		for i in range(num_skills):
			time_diff[mode][i]["text"] = ""
		result[mode]["text"] = ""
		if mode == 1:
			TRI_frames_frame.grid_remove()
		elif mode == 3:
			TRS_frames_frame.grid_remove()
		return
	for i in range(num_skills):
		if mode == 0:
			skill_total = max(calculate_time_times(TRI_start_time[i].get(),TRI_end_time[i].get()),0)
		elif mode == 1:
			skill_total = abs(calculate_time_fps(TRI_frame_diff[i].get(),fps))
		elif mode == 2:
			skill_total = abs(calculate_time_times(TRS_start_time[i].get(),TRS_end_time[i].get()))*2.5
		if mode == 3:
			skill_total = abs(calculate_time_fps(TRS_frame_diff[i].get(),fps))*2.5
		if (mode == 2 or mode == 3) and skill_total>1:
			time_diff[mode][i]["text"] = "Out of "+str(i)
			for j in range(i+1,num_skills):
				time_diff[mode][j]["text"] = ""
			num_skills_complete = i
			break
		else:
			total += skill_total
			time_diff[mode][i]["text"] = "{:.3f}".format(round(skill_total*1000)/1000)  #round to 3 decimal places
	if mode == 2 or mode == 3:
		total = num_skills_complete-total
	total = trunc(round(total*1000)/10)/100 #round to 3, truncate to 2 decimal places
	result[mode]["text"] = "{:.2f}".format(total)

def clear_scores():
	mode = mode_num()
	for i in range(num_skills):
		if mode == 0:
			TRI_start_time[i].set("0.0")
			TRI_end_time[i].set("0.0")
		elif mode == 1:
			TRI_frame_diff[i].set("0")
		if mode == 2:
			TRS_start_time[i].set("0.0")
			TRS_end_time[i].set("1.0")
		if mode == 3:
			fps = num_fps.get()
			TRS_frame_diff[i].set(str(fps))
	calculate_score()

#Validates entry as a number with max 1 decimal
def is_num(char_string):
	if len(char_string)>1:
		char = char_string[-1]
		decimal_present = "." in char_string[:-1]
	else:
		char = char_string
		decimal_present = False
	if str.isdigit(char) or char == "" or (char == "." and not decimal_present):
		return True
	else:
		return False

#Validates entry as a integer
def is_int(char_string):
	if len(char_string)>1:
		char = char_string[-1]
	else:
		char = char_string
	if str.isdigit(char) or char == "":
		return True
	else:
		return False

if sys.platform == "darwin":
	#mac
	entry_width = 5
	label_width = 8
	col_padding = 5
	large_font_size = 25
	theme_name = 'aqua'
elif sys.platform == "win32":
	#windows
	entry_width = 5
	label_width = 8
	col_padding = 5
	large_font_size = 18
	theme_name = 'vista'
else:
	raise Exception("Not configured to run on "+sys.platform)

### Prepare window
window = tk.Tk()
window.title("TOF Calculator")
window.resizable(width=True, height=True)
style = ttk.Style(window)
style.theme_use(theme_name)
window.geometry("350x450")
### Initialize Variables
num_skills = 10
num_cases = 4 #TRI time/frames, TRS time/frames
time_diff = [[0 for _ in range(num_skills)] for _ in range(num_cases)]
result = [0 for _ in range(num_cases)]
#For options
calc_type = tk.IntVar()
event_type = tk.IntVar()
num_frames = tk.IntVar()
#For TRI time
TRI_start_time_entry = ["" for _ in range(num_skills)]
TRI_start_time = [tk.StringVar() for _ in range(num_skills)]
TRI_end_time_entry = ["" for _ in range(num_skills)]
TRI_end_time = [tk.StringVar() for _ in range(num_skills)]
#For TRI frames
TRI_frames_diff_entry = ["" for _ in range(num_skills)]
TRI_frame_diff = [tk.StringVar() for _ in range(num_skills)]
TRI_frames_time_diff = [0 for _ in range(num_skills)]
#For TRS time
TRS_start_time_entry = ["" for _ in range(num_skills)]
TRS_start_time = [tk.StringVar() for _ in range(num_skills)]
TRS_end_time_entry = ["" for _ in range(num_skills)]
TRS_end_time = [tk.StringVar() for _ in range(num_skills)]
#For TRS frames
TRS_frames_diff_entry = ["" for _ in range(num_skills)]
TRS_frame_diff = [tk.StringVar() for _ in range(num_skills)]
TRS_frames_time_diff = [0 for _ in range(num_skills)]
# ### Background Frame
# background_frame = ttk.Frame(window)
# background_frame.grid(fill="both", expand=True)
### Options Frame
options_frame = ttk.Frame(master=window)
options_frame.grid(row=0, column=0, sticky=tk.S)
row_num = 0
ttk.Radiobutton(master=options_frame, text="Individual", variable=event_type, value=0).grid(row=row_num,column=0)
ttk.Radiobutton(master=options_frame, text="Synchro", variable=event_type, value=1).grid(row=row_num,column=1)
row_num += 1
ttk.Radiobutton(master=options_frame, text="Time", variable=calc_type, value=0).grid(row=row_num,column=0)
ttk.Radiobutton(master=options_frame, text="Frames", variable=calc_type, value=1).grid(row=row_num,column=1)
num_fps = ttk.Entry(master=options_frame, textvariable=num_frames, width=4, justify='center')
num_fps.config(validate='all', validatecommand=(num_fps.register(is_int), '%P'))
num_fps.grid(row=row_num,column=2)
num_frames.set(default_num_frames)
fps_label = ttk.Label(master=options_frame, text="fps")
fps_label.grid(row=row_num, column=3)
row_num += 1
fps_error_indicator = ttk.Label(master=options_frame, text="FPS must be greater than 0", font=("Arial", large_font_size))
fps_error_indicator.grid(row=row_num, column=0, columnspan = 3)
### TRI Time Frame
mode = 0
row_num = 0
TRI_time_frame = ttk.Frame(master=window)
ttk.Label(master=TRI_time_frame, text="Skill").grid(row=row_num, column=0)
ttk.Label(master=TRI_time_frame, text="Take-Off Time").grid(row=row_num, column=1)
ttk.Label(master=TRI_time_frame, text="Landing Time").grid(row=row_num, column=2)
ttk.Label(master=TRI_time_frame, text="Score").grid(row=row_num, column=3)
row_num += 1
for i in range(num_skills):
	tk.Label(master=TRI_time_frame, text=str(i+1)+":").grid(row=row_num+i, column=0)
	TRI_start_time_entry[i] = ttk.Entry(master=TRI_time_frame, textvariable=TRI_start_time[i], width=entry_width, justify='center')
	TRI_start_time_entry[i].config(validate='all', validatecommand=(TRI_start_time_entry[i].register(is_num), '%P'))
	TRI_start_time_entry[i].grid(row=row_num+i, column=1, sticky=tk.W+tk.E, padx=col_padding)
	TRI_end_time_entry[i] = ttk.Entry(master=TRI_time_frame, textvariable=TRI_end_time[i], width=entry_width, justify='center')
	TRI_end_time_entry[i].config(validate='all', validatecommand=(TRI_end_time_entry[i].register(is_num), '%P'))
	TRI_end_time_entry[i].grid(row=row_num+i, column=2, sticky=tk.W+tk.E, padx=col_padding)
	time_diff[mode][i] = ttk.Label(master=TRI_time_frame, text="0.00", width=label_width, anchor='center')
	time_diff[mode][i].grid(row=row_num+i, column=3, sticky=tk.W+tk.E, padx=col_padding)
row_num += num_skills
clear_button = ttk.Button(master=TRI_time_frame, text="Clear", command=clear_scores)
clear_button.grid(row=row_num, column=2)
result[mode] = ttk.Label(master=TRI_time_frame, text="0.00")
result[mode].grid(row=row_num, column=3, pady=5)
### TRI Frames Frame
mode = 1
row_num = 0
TRI_frames_frame = ttk.Frame(master=window)
ttk.Label(master=TRI_frames_frame, text="Skill").grid(row=row_num, column=0)
ttk.Label(master=TRI_frames_frame, text="Num Frames").grid(row=row_num, column=1)
ttk.Label(master=TRI_frames_frame, text="Score").grid(row=row_num, column=2)
row_num += 1
for i in range(num_skills):
	tk.Label(master=TRI_frames_frame, text=str(i+1)+":").grid(row=row_num+i, column=0)
	TRI_frames_diff_entry[i] = ttk.Entry(master=TRI_frames_frame, textvariable=TRI_frame_diff[i], width=entry_width, justify='center')
	TRI_frames_diff_entry[i].config(validate='all', validatecommand=(TRI_frames_diff_entry[i].register(is_num), '%P'))
	TRI_frames_diff_entry[i].grid(row=row_num+i, column=1, sticky=tk.W+tk.E, padx=col_padding)
	time_diff[mode][i] = ttk.Label(master=TRI_frames_frame, text="0.00", width=label_width, anchor='center')
	time_diff[mode][i].grid(row=row_num+i, column=2, sticky=tk.W+tk.E, padx=col_padding)
row_num += num_skills
clear_button = ttk.Button(master=TRI_frames_frame, text="Clear", command=clear_scores)
clear_button.grid(row=row_num, column=1)
result[mode] = ttk.Label(master=TRI_frames_frame, text="0.00")
result[mode].grid(row=row_num, column=2, pady=5)
### TRS Time Frame
mode = 2
row_num = 0
TRS_time_frame = tk.Frame(master=window)
ttk.Label(master=TRS_time_frame, text="Skill").grid(row=row_num, column=0)
ttk.Label(master=TRS_time_frame, text="Landing Time 1").grid(row=row_num, column=1)
ttk.Label(master=TRS_time_frame, text="Landing Time 2").grid(row=row_num, column=2)
ttk.Label(master=TRS_time_frame, text="Deduction").grid(row=row_num, column=3)
row_num += 1
for i in range(num_skills):
	tk.Label(master=TRS_time_frame, text=str(i+1)+":").grid(row=row_num+i, column=0)
	TRS_start_time_entry[i] = ttk.Entry(master=TRS_time_frame, textvariable=TRS_start_time[i], width=entry_width, justify='center')
	TRS_start_time_entry[i].config(validate='all', validatecommand=(TRS_start_time_entry[i].register(is_num), '%P'))
	TRS_start_time_entry[i].grid(row=row_num+i, column=1, sticky=tk.W+tk.E, padx=col_padding)
	TRS_end_time_entry[i] = ttk.Entry(master=TRS_time_frame, textvariable=TRS_end_time[i], width=entry_width, justify='center')
	TRS_end_time_entry[i].config(validate='all', validatecommand=(TRS_end_time_entry[i].register(is_num), '%P'))
	TRS_end_time_entry[i].grid(row=row_num+i, column=2, sticky=tk.W+tk.E, padx=col_padding)
	time_diff[mode][i] = ttk.Label(master=TRS_time_frame, text="0.00", width=label_width, anchor='center')
	time_diff[mode][i].grid(row=row_num+i, column=3, sticky=tk.W+tk.E, padx=col_padding)
row_num += num_skills
clear_button = tk.Button(master=TRS_time_frame, text="Clear", command=clear_scores)
clear_button.grid(row=row_num, column=2)
result[mode] = tk.Label(master=TRS_time_frame, text="0.00")
result[mode].grid(row=row_num, column=3, pady=5)
### TRS Frames Frame
mode = 3
row_num = 0
TRS_frames_frame = tk.Frame(master=window)
ttk.Label(master=TRS_frames_frame, text="Skill").grid(row=row_num, column=0)
ttk.Label(master=TRS_frames_frame, text="Frames Difference").grid(row=row_num, column=1)
ttk.Label(master=TRS_frames_frame, text="Deduction").grid(row=row_num, column=2)
row_num += 1
for i in range(num_skills):
	ttk.Label(master=TRS_frames_frame, text=str(i+1)+":").grid(row=row_num+i, column=0)
	TRS_frames_diff_entry[i] = ttk.Entry(master=TRS_frames_frame, textvariable=TRS_frame_diff[i], width=entry_width, justify='center')
	TRS_frames_diff_entry[i].config(validate='all', validatecommand=(TRS_frames_diff_entry[i].register(is_num), '%P'))
	TRS_frames_diff_entry[i].grid(row=row_num+i, column=1, sticky=tk.W+tk.E, padx=col_padding)
	time_diff[mode][i] = ttk.Label(master=TRS_frames_frame, text="0.00", width=label_width, anchor='center')
	time_diff[mode][i].grid(row=row_num+i, column=2, sticky=tk.W+tk.E, padx=col_padding)
row_num += num_skills
clear_button = tk.Button(master=TRS_frames_frame, text="Clear", command=clear_scores)
clear_button.grid(row=row_num, column=1)
result[mode] = tk.Label(master=TRS_frames_frame, text="0.00")
result[mode].grid(row=row_num, column=2, pady=5)
### Add frames to window
TRI_time_frame.grid(row=1, column=0, padx=10, sticky=tk.N)
TRI_frames_frame.grid(row=1, column=0, padx=10, sticky=tk.N)
TRS_time_frame.grid(row=1, column=0, padx=10, sticky=tk.N)
TRS_frames_frame.grid(row=1, column=0, padx=10, sticky=tk.N)
### Add traces to watch for value changes
for i in range(num_skills):
	TRI_start_time[i].trace_add('write', calculate_score)
	TRI_end_time[i].trace_add('write', calculate_score)
	TRI_frame_diff[i].trace_add('write', calculate_score)
	TRS_start_time[i].trace_add('write', calculate_score)
	TRS_end_time[i].trace_add('write', calculate_score)
	TRS_frame_diff[i].trace_add('write', calculate_score)
	num_frames.trace_add('write', calculate_score)
calc_type.trace_add('write', change_calc_type)
event_type.trace_add('write', change_calc_type)
### Configure column widths and row heights when resizing
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
for j in range(4):
	TRI_time_frame.columnconfigure(j, weight=1)
	TRI_frames_frame.columnconfigure(j, weight=1)
	TRS_time_frame.columnconfigure(j, weight=1)
	TRS_frames_frame.columnconfigure(j, weight=1)
	options_frame.columnconfigure(j, weight=1)
for i in range(2):
	options_frame.rowconfigure(i, weight=1)
for i in range(num_skills+2):
	TRI_time_frame.rowconfigure(i, weight=1)
	TRI_frames_frame.rowconfigure(i, weight=1)
	TRS_time_frame.rowconfigure(i, weight=1)
	TRS_frames_frame.rowconfigure(i, weight=1)
### Show Window with only TRI Time frame
for i in range(2):
	for j in range(2):
		calc_type.set(i)
		event_type.set(j)
		clear_scores()
calc_type.set(0)
event_type.set(0)
change_calc_type()
window.mainloop()
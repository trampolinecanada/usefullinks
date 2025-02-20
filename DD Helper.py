import tkinter as tk
from math import trunc
from functools import partial
import sys

#Format options
gui_background_color = '#323232' #grey
text_colour = 'white'
highlight_colour = '#D32027' #gymcan red
background_colour = 'black'
button_text_colour = 'black'
female_colour = '#F608FF' #magenta
male_colour = '#5DD4FC' #cyan
font = 'sans 14 bold'
frames_on = False #For debugging
#GUI size parameters
entry_width = 8
label_width = 8
col_padding = 5
button_width = 5
button_border_width = 2

def calculate_DD(skill_string):
	try:
		if skill_string == "":
			return 0
		#Parse skill string
		could_be_backwards = True
		if skill_string[0] == ".":
			could_be_backwards = False
			skill_string = skill_string[1:]
		skill_string = skill_string.replace("-","0")
		if len(skill_string) == 2:
			flips = int(skill_string[0])
			twists = int(skill_string[1])
			position = "/"
		elif len(skill_string) == 3:
			flips = int(skill_string[0])
			twists = int(skill_string[1])
			position = skill_string[2]
		elif len(skill_string) == 4:
			flips = int(skill_string[0])
			twists = int(skill_string[1])+int(skill_string[2])
			position = skill_string[3]
		elif len(skill_string) == 5:
			flips = int(skill_string[0:2])
			twists = int(skill_string[2])+int(skill_string[3])
			position = skill_string[4]
		elif len(skill_string) == 6:
			flips = int(skill_string[0:2])
			twists = int(skill_string[2])+int(skill_string[3])+int(skill_string[4])
			position = skill_string[5]
		elif len(skill_string) == 7:
			flips = int(skill_string[0:2])
			twists = int(skill_string[2])+int(skill_string[3])+int(skill_string[4])+int(skill_string[5])
			position = skill_string[6]
		# DD for flipping
		DD = flips
		if flips > 3:
			DD += 1
		if flips > 7:
			DD += 1
		if flips > 11:
			DD += 2
		if flips > 15:
			DD += 2
		DD += twists
		# DD for position
		if position in "</":
			if flips > 7:
				DD += (flips-flips%4)//4
			elif flips > 3 and twists == 0:
				DD += 1
		# Twisting bonus
		if flips > 15:
			DD += twists*2
		elif flips > 11:
			if twists > 2:
				DD += (twists-2)*2
		elif flips > 7:
			if twists > 4:
				DD += twists-4		
		# Back skill bonus
		if twists%2 == 0 and could_be_backwards:
			if flips > 15:
				DD += 3
			elif flips > 11:
				DD += 2
			elif flips > 7:
				DD += 1
		if DD == 0:
			DD += 1
		return DD/10
	except:
		return 0.1

def calculate_total(*args):
	total = 0
	for score in score_strings:
		s = score.get()
		if s != "":
			total += float(s)
	total = round(total*10)/10 #round to 1 decimal place
	result["text"] = "{:.1f}".format(total)
	#calculate bonus
	num_triples = 0
	for skill in skill_strings:
		skill_string = skill.get()
		if skill_string != "":
			if skill_string[0] == ".":
				skill_string = skill_string[1:]
			if len(skill_string) > 4:
				num_triples += 1
	bonus_w_value = max(0,(num_triples-2)*0.3)
	bonus_m_value = max(0,(num_triples-5)*0.3)
	bonus_women["text"] = "{:.1f}".format(bonus_w_value)
	bonus_men["text"] = "{:.1f}".format(bonus_m_value)
	total_women["text"] = "{:.1f}".format(bonus_w_value+total)
	total_men["text"] = "{:.1f}".format(bonus_m_value+total)

def update_score(n=-1,*args):
	if n>=0:
		score_entry[n].configure(bg=background_colour,fg=text_colour)
		skill_string = skill_strings[n].get()
		skill_total = calculate_DD(skill_string)
		score_strings[n].set("{:.1f}".format(round(skill_total*10)/10))  #round to 1 decimal place
		if skill_string != "" and skill_string in [skill_strings[i].get() for i in range(n)]:
			score_strings[n].set("0")
			score_entry[n].configure(bg=background_colour,fg=highlight_colour)

def clear_scores():
	for i in range(num_skills):
		skill_strings[i].set("")

def enter_skill(skill_string):
	for i in range(len(skill_strings)):
		if skill_strings[i].get() == "":
			skill_strings[i].set(skill_string)
			return

def on_enter(obj):
	obj.widget['fg']=highlight_colour

def on_leave(obj):
	obj.widget['fg']=button_text_colour

def create_skill_button_frame(title,skills,row,col,rowspan=1):
	button_frame = tk.Frame(master=elements_frame, borderwidth=2) #highlightbackground="black", highlightthickness=1
	frame_list.append(button_frame)
	button_frame.configure(background=gui_background_color)
	button_frame.grid(row=row, rowspan=rowspan, column=col, padx=10, pady=10)
	skill_buttons = ["" for _ in skills]
	if title != "":
		tk.Label(master=button_frame, text=title, fg=text_colour, font=font, background=gui_background_color).grid(row=0, column=0)
	for i in range(len(skills)):
		skill_buttons[i] = tk.Button(master=button_frame, text=skills[i], command=partial(enter_skill, skills[i]), fg=button_text_colour, font=font, bd=button_border_width)
		skill_buttons[i].grid(row=i+1, column=0)
		skill_buttons[i].config(width=button_width, height=2)
		skill_buttons[i].bind("<Enter>",on_enter)
		skill_buttons[i].bind("<Leave>",on_leave)
	for i in range(len(skills)+1):
		button_frame.rowconfigure(i, weight=1)
	return button_frame

frame_list = []
### Prepare window
window = tk.Tk()
window.title("DD Helper")
window.resizable(width=True, height=True)
window.geometry("1400x800")
window.configure(background=gui_background_color)
### Initialize Variables
num_skills = 10
# values = [0 for _ in range(num_skills)]
scores = [0 for _ in range(num_skills)]
result = 0
FIG_code_entry = ["" for _ in range(num_skills)]
score_entry = ["" for _ in range(num_skills)]
skill_strings = [tk.StringVar() for _ in range(num_skills)]
score_strings = [tk.StringVar() for _ in range(num_skills)]
### Skill Frame
row_num = 0
DD_frame = tk.Frame(master=window)
DD_frame.configure(background=gui_background_color)
frame_list.append(DD_frame)
tk.Label(master=DD_frame, text="Element", fg=text_colour, font=font, background=gui_background_color).grid(row=row_num, column=0)
tk.Label(master=DD_frame, text="FIG Code", fg=text_colour, font=font, background=gui_background_color).grid(row=row_num, column=1)
tk.Label(master=DD_frame, text="Score", fg=text_colour, font=font, background=gui_background_color).grid(row=row_num, column=2)
row_num += 1
for i in range(num_skills):
	tk.Label(master=DD_frame, text=str(i+1)+":", fg=text_colour, font=font, background=gui_background_color).grid(row=row_num+i, column=0)
	FIG_code_entry[i] = tk.Entry(master=DD_frame, textvariable=skill_strings[i], width=entry_width, justify='center', font=font, bd=0, bg='black')
	FIG_code_entry[i].grid(row=row_num+i, column=1, sticky=tk.W+tk.E, padx=col_padding)
	FIG_code_entry[i].config(bg=background_colour,fg=text_colour)
	score_entry[i] = tk.Entry(master=DD_frame, textvariable=score_strings[i], width=entry_width, justify='center', font=font, bd=0, bg='black')
	score_entry[i].grid(row=row_num+i, column=2, sticky=tk.W+tk.E, padx=col_padding)
	score_entry[i].config(bg=background_colour,fg=text_colour)
row_num += num_skills
clear_button = tk.Button(master=DD_frame, text="Clear", command=clear_scores, width=button_width, fg=button_text_colour, font=font, bd=button_border_width)
clear_button.grid(row=row_num, column=1)
clear_button.bind("<Enter>",on_enter)
clear_button.bind("<Leave>",on_leave)
result = tk.Label(master=DD_frame, text="0.0", fg=text_colour, font=font, background=gui_background_color)
result.grid(row=row_num, column=2, pady=5)
row_num += 1
tk.Label(master=DD_frame, text="Bonus F:", fg=text_colour, font=font, background=gui_background_color).grid(row=row_num, column=0, pady=5)
bonus_women = tk.Label(master=DD_frame, text="0.0", fg=text_colour, font=font, background=gui_background_color)
bonus_women.grid(row=row_num, column=1, pady=5)
total_women = tk.Label(master=DD_frame, text="0.0", fg=female_colour, font=font, background=gui_background_color)
total_women.grid(row=row_num, column=2, pady=5)
row_num += 1
tk.Label(master=DD_frame, text="Bonus M:", fg=text_colour, font=font, background=gui_background_color).grid(row=row_num, column=0, pady=5)
bonus_men = tk.Label(master=DD_frame, text="0.0", fg=text_colour, font=font, background=gui_background_color)
bonus_men.grid(row=row_num, column=1, pady=5)
total_men = tk.Label(master=DD_frame, text="0.0", fg=male_colour, font=font, background=gui_background_color)
total_men.grid(row=row_num, column=2, pady=5)
### Element Buttons Frame
elements_frame = tk.Frame(master=window)
elements_frame.configure(background=gui_background_color)
frame_list.append(elements_frame)
col = 0

col += 1
# non_flipping_frame = create_skill_button_frame("Non-flipping",["--o","--<","--v","--L","-1L","--u","-1u","1-F","1-B","11F"],0,col,3)
jump_frame = create_skill_button_frame("Jumps",["--o","--<","--v"],0,col)
seat_frame = create_skill_button_frame("Seat",["--L","-1L","--↑","-1↑"],1,col)
back_front_frame = create_skill_button_frame("Back/Front",["1-B","1-F","11F"],2,col)

col += 1
quarter_flipping_frame = create_skill_button_frame("3/4 skills",["3-/","7--o","7--<","5-o","51o"],0,col,3)

col += 1
singles_frame = create_skill_button_frame("Singles",[],0,col)
singles_frame = create_skill_button_frame("Doubles",[],1,col)
singles_frame = create_skill_button_frame("Triples",[],2,col)

col += 1
zero_singles_frame = create_skill_button_frame("0 twist",["4-o","4-<","4-/"],0,col)
zero_doubles_frame = create_skill_button_frame("",["8--o","8--<","8--/"],1,col)
zero_triples_frame = create_skill_button_frame("",["12---o","12---<"],2,col)

col += 1
one_singles_frame = create_skill_button_frame("1 twist",["41o","41<","41/"],0,col)
one_doubles_frame = create_skill_button_frame("",["8-1o","8-1<"],1,col)
one_triples_frame = create_skill_button_frame("",["12--1o","12--1<"],2,col)

col += 1
two_singles_frame = create_skill_button_frame("2 twist",["42"],0,col)
two_doubles_frame = create_skill_button_frame("",["811o","811<","8-2o","8-2<","8-2/"],1,col)
two_triples_frame = create_skill_button_frame("",["121-1o","121-1<"],2,col)

col += 1
three_singles_frame = create_skill_button_frame("3 twist",["43"],0,col)
three_doubles_frame = create_skill_button_frame("",["8-3o","8-3<","821o","821<","821/"],1,col)
three_triples_frame = create_skill_button_frame("",["12--3o","12--3<","122-1o","122-1<"],2,col)

col += 1
four_singles_frame = create_skill_button_frame("4 twist",["44"],0,col)
four_doubles_frame = create_skill_button_frame("",["813o","813<","822o","831<","822/"],1,col)
four_triples_frame = create_skill_button_frame("",["121-3o","121-3<","123-1o","123-1<"],2,col)

col += 1
five_singles_frame = create_skill_button_frame("5 twist",["45"],0,col)
five_doubles_frame = create_skill_button_frame("",["8-5<","823/"],1,col)

col += 1
six_singles_frame = create_skill_button_frame("6 twist",["46"],0,col)
six_doubles_frame = create_skill_button_frame("",["833/"],1,col)

col_max = col
row_max = 2
### Add frames to window
DD_frame.grid(row=1, column=1, padx=10)
elements_frame.grid(row=1, column=2, padx=10, sticky=tk.N+tk.W)
### Add traces to watch for value changes
for i in range(num_skills):
	skill_strings[i].trace_add('write', partial(update_score,i))
	score_strings[i].trace_add('write',calculate_total)
### Configure column widths and row heights when resizing
for i in range(3):
	window.rowconfigure(i, weight=1)
for j in range(3):
	window.columnconfigure(j, weight=1)
for i in range(num_skills+2):
	DD_frame.rowconfigure(i, weight=1)
for j in range(3):
	DD_frame.columnconfigure(j, weight=1)
for i in range(col_max+1):
	elements_frame.rowconfigure(i, weight=1)
for j in range(col_max+1):
	elements_frame.columnconfigure(j, weight=1)
if frames_on:
	for f in frame_list:
		f.configure(highlightbackground="black", highlightthickness=1)
### Show Window
clear_scores()
window.mainloop()
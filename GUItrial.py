from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from control_class import DSP
from functools import partial

try:
	import RPi.GPIO as GPIO

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(10, GPIO.OUT)
	GPIO.output(10, GPIO.LOW)
except Exception:
	print("GPIO library could not be loaded!")
	class GPIO:
		def input(self, value):
			print("pin ",value,"set as input")
		def output(self, value1, value2):
			print("pin ",value,"set as output",value2)

def toggle():
	if GPIO.input(10):
		GPIO.output(10, GPIO.LOW)
		toggleButton["text"] = "Adjust values for Gain"

def info_msg(info):
	messagebox.showwarning(info)

def unfinished(holder=''):
	messagebox.showwarning("TODO","this has not yet been programmed") 

# Keyboard reference:
# https://www.daniweb.com/programming/software-development/threads/300867/on-screen-keyboards-in-tkinter#

def click(btn):
	"""Enters the selected button character in the text entry field.
	Still need to add backspace (TODO)"""
	s = "Button %s clicked" % btn
	E1.insert(INSERT, btn)
	root.title(s)

root = Tk()
root['bg'] = 'black'
root.geometry('800x480')
#root.attributes('-fullscreen',True) # Uncomment when moved to rpi

Lframe = Frame(root, bd=3,bg='black')
Lframe.pack(side='left')
Cframe = Frame(root, bd=3)#, bg='steelblue3')
Cframe.pack(side='left', expand = True, fill=BOTH)
Rframe = Frame(root, bd=3, bg='black')
Rframe.pack(side='left', fill=BOTH)


topframe = LabelFrame(Cframe, text = " Menu buttons ", bd=3)
topframe.pack(padx=15, pady=10)

midframe = LabelFrame(Cframe, text = " Code entry ", bd=3)
midframe.pack(padx=15, pady=10)

tool_button = ttk.Button(topframe, text= "Tools", command=unfinished)
tool_button.pack(padx=10,side='left')
home_button = ttk.Button(topframe, text= "Home", command=unfinished)
home_button.pack(padx=10,side='left')
load_button = ttk.Button(topframe, text= "Load Preset", command=unfinished)
load_button.pack(padx=10,side='left')
save_button = ttk.Button(topframe, text= "Save", command=unfinished)
save_button.pack(padx=10,side='left')


E1 = Text(midframe,wrap=NONE, height = 12, width = 64)
E1.pack(fill=BOTH, expand = True)

# Sample equation 
E1.insert(INSERT, """#Click buttons!\nDSP.output[1].mute = control.button3""")

bottomframe = LabelFrame(Cframe, text=" keypad ", bd=3)
bottomframe.pack(padx=15, pady=10)
# typical calculator button layout
btn_list = [
['+', '-', '*', '/', '^', '%', '(', ')', '='],
['1',  '2',  '3',  '4',  '5', '6', '7', '8', '9', '0', '-', '+'],
['Q',  'W',  'E',  'R',  'T', 'Y', 'U', 'I', 'O', 'P', '[', ']'],
['A',  'S',  'D',  'F',  'G', 'H', 'J', 'K', 'L', ';', '"'],
['Z',  'X',  'C',  'V',  'B', 'N', 'M', ',', '.', '/' ]]

n = 0 # loop counter variable

btn = list(range(sum(map(len,btn_list))))
for sub in btn_list:
	for label in sub:
		# partial takes care of function and argument
		cmd = partial(click, label)
		# create the button
		btn[n] = ttk.Button(bottomframe, text=label, width=5, command=cmd)
		# position the button
		btn[n].grid(row=btn_list.index(sub), column=sub.index(label))
		# increment button index
		n += 1


# I/O buttons

inbuttons = []
outbuttons = []

for i in DSP.input:
	cmd = partial(click, i.id)
	inbuttons.append(ttk.Button(Lframe, text='\n'+i.name+'\n', command=cmd))
	inbuttons[-1].pack(padx = 5, pady=2, fill=BOTH)#, expand=True)
for o in DSP.output:
	cmd = partial(click, o.id)
	outbuttons.append(ttk.Button(Rframe, text='\n'+o.name+'\n', command=cmd))
	outbuttons[-1].pack(padx = 5, pady=2, fill=BOTH)#, expand=True)


root.mainloop()
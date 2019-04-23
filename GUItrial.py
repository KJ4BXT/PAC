from tkinter import *
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO,setup(10, GPIO.OUT)
GPIO.output(10, GPIO.LOW)

def toggle():
	if GPIO.input(10):
		GPIO.output(10, GPIO.LOW)
		toggleButton["text"] = "Adjust values for Gain"
		

root = Tk()

global enteredtext
global texttry

enteredtext = " ";
def keyentered(event):
	#texttry [:-1] = 1
	print (texttry)
	print(enteredtext)
	#enteredtext = text
	#return(enteredtext)

texttry = Text(root, height = 4, width = 60)
texttry.grid(row = 0, columnspan=10)

L = label(root,text="Thank you for chosing PAC as your Primer Audio Controller")
L.pack()

f1 = Frame(root)
f1.grid(row=1, sticky="nsew")

q = Button(f1, text = "q")
q.bind('<Button-1>',keyentered)
q.grid(row = 1, column=1,sticky="ew")

w = Button(f1, text = "w")
w.bind('<Button-1>',keyentered)
w.grid(row= 1, column=2,sticky="ew")

e = Button(f1, text = "e")
e.bind('<Button-1>',keyentered)
e.grid(row= 1, column=3,sticky="ew")

r = Button(f1, text = "r")
r.bind('<Button-1>',keyentered)
r.grid(row= 1, column=4,sticky="ew")

t = Button(f1, text = "t")
t.bind('<Button-1>',keyentered)
t.grid(row= 1, column=5,sticky="ew")

y = Button(f1, text = "y")
y.bind('<Button-1>',keyentered)
y.grid(row= 1, column=6,sticky="ew")

u = Button(f1, text = "u")
u.bind('<Button-1>',keyentered)
u.grid(row= 1, column=7,sticky="ew")

i = Button(f1, text = "i")
i.bind('<Button-1>',keyentered)
i.grid(row= 1, column=8,sticky="ew")

o = Button(f1, text = "o")
o.bind('<Button-1>',keyentered)
o.grid(row= 1, column=9,sticky="ew")

p = Button(f1, text = "p")
p.bind('<Button-1>',keyentered)
p.grid(row= 1, column=10,sticky="ew")


#Row 2 creation
r2vals = "asdfghjkl;\""
r2buttons = []

for i in r2vals:
	r2buttons.append(Button(f1, text=i))

for i in range(len(r2buttons)):
	r2buttons[i].bind(r2buttons[i], keyentered)
	r2buttons[i].grid(row=2,column=i,sticky="ew")

root.mainloop()

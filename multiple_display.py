import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import adafruit_tca9548a
from time import sleep

# Display size
WIDTH = 128
HEIGHT = 64
BORDER = 5

i2c = board.I2C()
tca = [adafruit_tca9548a.TCA9548A(i2c,address=0x70),adafruit_tca9548a.TCA9548A(i2c,address=0x71)]

disp = [] # Display list

#Set up displays
for i in range(14):
	try:
		disp.append(adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, tca[i//7][i%7], addr=0x3c))
	except Exception as e:
		disp.append(None)
		print('oled setup failed, index ',i,'on tca module 0-2: ',i//7)

def show(ind, text):
	global disp
	fontsize = 24 # arbitrary static
	font = ImageFont.truetype("Calibri.ttf",fontsize) #if it does set font size appropriately using Calibri.

	if (type(ind) != int):
		raise TypeError('display selector must be an integer')
	#Start of drawing
	try:
		image = Image.new('1', (disp[ind].width, disp[ind].height))
		draw = ImageDraw.Draw(image)

		disp[ind].fill(0)
		if (type(text) == str): # Single line
			if (len(text) > 11):
				print("warning: string length unsupported")
				text = text[:11]
			(font_width, font_height) = font.getsize(text)
			draw.text((disp[ind].width//2 - font_width//2, disp[ind].height//2 - font_height//2), 
				text, font=font, fill=255)

			disp[ind].image(image)
			disp[ind].show()

		if (type(text) == list): # 2 lines
			if (len(text) > 2):
				text = text[:2] #only two lines of text
			for i in range(len(text)):
				if (len(text[i]) > 11):
					print("warning: string length unsupported. Text Truncated")
					text[i] = text[i][:11] # Clip to 11 characters
				(font_width, font_height) = font.getsize(text[i])
				draw.text((disp[ind].width//2 - font_width//2, (i*2+1)*disp[ind].height//4 - font_height//2),
		          		text[i], font=font, fill=255)

			disp[ind].image(image)
			disp[ind].show()
	except Exception as e:
		print("Could not write to display index ", ind, e)
		return(-1)

def ID(): # Show display index on each screen
	for i in range(len(disp)):
		show(i,[str(i),''])

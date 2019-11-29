import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import adafruit_tca9548a
from time import sleep

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Display size
WIDTH = 128
HEIGHT = 64
BORDER = 5

i2c = board.I2C()

tca = [adafruit_tca9548a.TCA9548A(i2c,address=0x70),adafruit_tca9548a.TCA9548A(i2c,address=0x71)]

disp = []

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
		if (type(text) == str):
			print('single string, top line')
		if (type(text) == list):
			print('multiple strings')
		
			for i in range(len(text)):
				(font_width, font_height) = font.getsize(text[i])
				draw.text((disp[ind].width//2 - font_width//2, (i*2+1)*disp[ind].height//4 - font_height//2),
		          		text[i], font=font, fill=255)

			disp[ind].image(image)
			disp[ind].show()
	except Exception as e:
		print("Could not write to display index ", ind)
		return(-1)

def ID():
	for i in range(len(disp)):
		show(i,[str(i),''])

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import adafruit_tca9548a
from time import sleep


# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Change these
# to the right size for your display!
WIDTH = 128
HEIGHT = 64     # Change to 64 if needed
BORDER = 5

# Use for I2C.
i2c = board.I2C()

tca = [adafruit_tca9548a.TCA9548A(i2c,address=0x70),adafruit_tca9548a.TCA9548A(i2c,address=0x71)]
#tca0 = adafruit_tca9548a.TCA9548A(i2c,address = 0x70)
#tca1 = adafruit_tca9548a.TCA9548A(i2c,address = 0x71)
#tca2 = adafruit_tca9548a.TCA9548A(i2c, addr=0x72) #add this for above 13
#tca = [tca0, tca1]

disp = []

#for i in range(11):
#display.append(adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, tca[0], addr=0x3c, reset=oled_reset))
#oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, tca[0], addr=0x3c, reset=oled_reset)

for i in range(14):
	try:
		disp.append(adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, tca[i//7][i%7], addr=0x3c, reset=oled_reset))
		#print('tca ',i//7)
	except Exception as e:
		disp.append(None)
		print('oled failed, ',i,'tca ',i//7)

#tsl1 = adafruit_tsl2591.TSL2591(tca[0])

# Use for SPI
#spi = board.SPI()
#oled_cs = digitalio.DigitalInOut(board.D5)
#oled_dc = digitalio.DigitalInOut(board.D6)
#oled = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, oled_dc, oled_reset, oled_cs)

def show(ind, text):
	global disp
	fontsize = 24 # arbitrary static
	font = ImageFont.truetype("Calibri.ttf",fontsize) #if it does set font size appropriately using Calibri.

	if (type(ind) != int):
		raise TypeError('display selector must be an integer')
	#Start of drawing
	image = Image.new('1', (disp[ind].width, disp[ind].height))
	draw = ImageDraw.Draw(image)

	disp[ind].fill(0)
	if (type(text) == str):
		print('single string, top line')
	if (type(text) == list):
		print('multiple strings')
		
		for i in range(len(text)):
			(font_width, font_height) = font.getsize(text[i])
			draw.text((disp[x].width//2 - font_width//2, (i*2+1)*disp[x].height//4 - font_height//2),
	          		text[i], font=font, fill=255)

		disp[ind].image(image)
		disp[ind].show()

i = 0
while True:
	x = 0
	#x = int(input('choose display: '))
	# Clear display.
	disp[x].fill(0)
#	disp[x].show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
	image = Image.new('1', (disp[x].width, disp[x].height))

# Get drawing object to draw on image.
	draw = ImageDraw.Draw(image)

# Draw a white background
#draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

# Draw a smaller inner rectangle
#draw.rectangle((BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
#               outline=0, fill=0)

# Load default font.
	#font = ImageFont.load_default()
	size = 20
	#size = int(input('font size: '))
	font = ImageFont.truetype("Calibri.ttf",size) #if it does set font size appropriately using Calibri.

# Draw Some Text
	text = str(i)
	(font_width, font_height) = font.getsize(text)
	draw.text((disp[x].width//2 - font_width//2, disp[x].height//4 - font_height//2),
	          text, font=font, fill=255)


	text = '1234567890'
	draw.text((0, 3*disp[x].height//4 - font_height//2),
	          text, font=font, fill=255)


# Display image
	disp[x].image(image)
	disp[x].show()
#	sleep(0.5)
	i += 1

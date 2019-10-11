import times
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import RPi.GPIO as GPIO

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


# Raspberry Pi pin configuration:
RST = 24


z = 1
# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Get display width and height.
width = disp.width
height = disp.height

# Clear display.
disp.clear()
disp.display()

# Create image buffer.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (width, height))


if z <100 and z>9:
    font = ImageFont.truetype("Calibri.ttf", 88)
if z >= 0 and z < 10:
    font = ImageFont.truetype("Calibri.ttf", 88)
if z == 100:
    font = ImageFont.truetype("Calibri.ttf", 80)


# Create drawing object.
draw = ImageDraw.Draw(image)
#text = '100', unused = draw.textsize(text, font=font)
draw.rectangle((0,0,width,height), outline=0, fill=0)
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

while True:
    
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)


        
    # Write two lines of text.

    draw.text((x, top), str(z),font=font, fill=255)
    
    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)


# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time
import smbus2
import board
import busio
import math
import adafruit_tca9548a

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

bus = smbus2.SMBus(1)

TCA_ADDR = 0x70 #mux address
TCA_PORT_DISPLAY1 = 0 #mux port

def mux_select(bus,tca_port):
    assert(0 <= tca_port <= 7)
    bus.write_byte(TCA_ADDR, 1 << tca_port)

# 128x32 display with hardware I2C:
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(mux_select(bus,TCA_PORT_DISPLAY1))#,rst=RST)

# Note you can change the I2C address by passing an i2c_address parameter like:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Alternatively you can specify an explicit I2C bus number, for example
# with the 128x32 display you would use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Alternatively you can specify a software SPI implementation by providing
# digital GPIO pin numbers for all the required display pins.  For example
# on a Raspberry Pi with the 128x32 display you might use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load Calibri font with varying size
font = ImageFont.truetype("Calibri.ttf",autosizetext(textlist)); #need to download calibri font so use this link: https://www.fontpalace.com/font-details/Calibri/

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
   #cmd = "hostname -I | cut -d\' \' -f1"
   # IP = subprocess.check_output(cmd, shell = True )
   # cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
   # CPU = subprocess.check_output(cmd, shell = True )
   # cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
   # MemUsage = subprocess.check_output(cmd, shell = True )
   # cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
   # Disk = subprocess.check_output(cmd, shell = True )

    # Write two lines of text.

    draw.text((x, top+1),       ,  font=font, fill=255)
    draw.text((x, top+1+fontsize),     , font=font, fill=255)
   # if TCA_PORT_DISPLAY1:
        #draw.text((x, top+16),    str(MemUsage.decode()),  font=font, fill=255)
        #draw.text((x, top+25),    str(Disk.decode()),  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
#    time.sleep(.25)
    TCA_PORT_DISPLAY1 = int(not TCA_PORT_DISPLAY1) #mux port
    disp = Adafruit_SSD1306.SSD1306_128_64(mux_select(bus,TCA_PORT_DISPLAY1))#,rst=RST)


#function to read list of messages and choose which OLED to display on using the display's number (dispnum) and the text to disp (text2disp)
 
def dispchoose(dispnum, text2disp)
    TCA_ADDR = 0x70 + hex(math.floor(dispnum/8)) #divide the display number by 8 to find which mux chip it is addressed to
    TCA_PORT_DISPLAY1 = dispnum%8 #use modulus of dispnum by 8 to determine the port number on the mux chip given by dnum.
    x,y = autosizetext(text2disp)
    numrows = len(y)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    if numrows == 1 # text can display on one row so display it using only one row
        draw.text((x, top+1),y[0],  font= x, fill=255)
    elif numrows == 2# need to display on two rows so write the text in two rows
        draw.text((x, top+1),y[0],  font= x, fill=255)
        draw.text((x, top+1+12),y[1],  font= x, fill=255)
    elif numrows == 3 # need to display on three rows so write the text in three rows
        draw.text((x, top+1),y[0],  font= x, fill=255)
        draw.text((x, top+13),y[1],  font= x, fill=255)    
        draw.text((x, top+25),y[2],  font= x, fill=255)
    elif numrows == 4 # need to display on four rows so write the text in four rows
        draw.text((x, top+1),y[0],  font= x, fill=255)
        draw.text((x, top+13),y[1],  font= x, fill=255) 
        draw.text((x, top+25),y[2],  font= x, fill=255)
        draw.text((x, top+37),y[3],  font= x, fill=255)   
    disp.image(image) #"draw" the text
    disp.display() #display the text
   # if dnum == 0
   #     TCA_ADDR = 0x70;
   # elif dnum == 1:
   #     TCA_ADDR = 0x71;
   # elif dnum == 2:
   #     TCA_ADDR = 0x72;
   # return(TCA_ADDR, TCA_PORT_DISPLAY1); # return the hex address and port for the OLED display to use. May be needed or may call autosizetext function here.

def autosizetext(text) # need to change to allow for space/null characters in text string and to scroll text. Also need to consider if multi-line text has < 17 characters on its following lines.
#    textlen = len(text);
    for i in text:
        textlen = len(text[i]); #determine how many characters are in the message
        fontsize = {1:76, 2:76, 3:63, 4:47, 5:41, 6:36, 7:30, 8:27, 9:23, 10:21, 11:19, 12:17,13:15, 14:15, 15:14, 16:13, 17:12} #dictionary to help set the font size
        if textlen <= 17: # check if text will fit on one line on the OLED.
            font = ImageFont.truetype("Calibri.ttf",fontsize[textlen]); #if it does set font size appropriately using Calibri.
            textl = text #the text fits on one row so no need to reformat
        elif textlen > 17:
            numlines = math.ceiling(textlen/17); #check how many lines are needed
            font = ImageFont.truetype("Calibri.ttf",fontsize[17]) #set font size 12
            if numlines == 2: # 2 lines are needed to display text
                textl = [text[0:16],text[17:34]] #create text list of two rows
            elif numlines == 3:
                textl = [text[0:16],text[17:34],text[35:52]] #text list of three rows
            elsif numlines == 4:
                textl = [text[0:16],text[17:34],text[35:52],text[53:70]] # text list of four rows


    return(font,textl);            


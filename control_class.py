#!/usr/bin/env python3

# Notes on how docstrings should be implemented:
# https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
# Please try to generally adhere to PEP8 coding standards.
# Tkinter imports may be an exception
# Callback example: 
# https://stackoverflow.com/questions/51885246/callback-on-variable-change-in-python

#Imports
from time import sleep
from math import acos, asin, atan, atan2, ceil, cos, degrees, e, exp, floor
from math import gcd, log, log10, pow, sqrt, sin, tan, radians, pi, tau
from datetime import datetime
from threading import Thread
import smbus2, board, busio
import RPi.GPIO as GPIO
from pyky040 import pyky040
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

bus = smbus2.SMBus(1)
i2c = busio.I2C(board.SCL, board.SDA)#, frequency=1000000)

GPIO.setmode(GPIO.BCM)

ADDR = 0x3B #DSP addresss

NUM_INPUTS = 4
NUM_OUTPUTS = 8
NUM_CONTROLS = 20 # Can probably delete this line

#Pin definitions
button0 = 15
button1 = 18
button2 = 23
button3 = 24
buttonmode = 'toggle' # alternative: 'momentary'

led0 = 20
led1 = 16
led2 = 12
led3 = 25

button = [0, 0, 0, 0] # button list
slider = [0, 0, 0, 0] # Faders
pot = [0, 0] # Potentiometers
rotary = [0, 0] # rotary encoders

commands = [] # This is the global variable to store the command queue

rot0CLK = 0
rot0DT = 0
rot0SW = 0
rot1CLK = 0
rot1DT = 0
rot1SW = 0

encoder = [pyky040.Encoder(CLK=rot0CLK,DT=rot0DT,SW=rot0SW),pyky040.Encoder(CLK=rot1CLK,DT=rot1DT,SW=rot1SW)]

# Binary inputs (toggle switches, buttons, etc.)
# should be set up using interrupts. 
# Need to ensure that interrupts do not interfere with writes in progress

def rotary_0(pos):
    rotary[0] = pos
def rotary_1(pos):
    rotary[1] = pos

encoder[0].setup(scale_min=0, scale_max=1, step=0.01, chg_callback=rotary_0)
encoder[1].setup(scale_min=0, scale_max=1, step=0.01, chg_callback=rotary_1)

rotwatch0 = Thread(target=encoder[0].watch, daemon=True)
rotwatch1 = Thread(target=encoder[1].watch, daemon=True)
rotwatch0.start()
rotwatch1.start()

def btn_ISR(pin): # Triggered on rising and falling
	if (buttonmode == 'momentary'):
		stat = GPIO.input(pin)
		if (pin == button0):
			button[0] = stat
		elif(pin == button1):
			button[1] = stat
		elif (pin == button2):
			button[2] = stat
		elif (pin == button3):
			button[3] = stat
	else: # toggle mode. May consider using elif
		if (pin == button0):
			button[0] = not button[0]
		elif(pin == button1):
			button[1] = not button[1]
		elif (pin == button2):
			button[2] = not button[2]
		elif (pin == button3):
			button[3] = not button[3]


for btn in [button0, button1, button2, button3]:
	GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(btn, GPIO.BOTH, callback=btn_ISR, bouncetime=250)

for led in [led0, led1, led2, led3]:
	GPIO.setup(led, GPIO.OUT)

adc = [ADS.ADS1115(i2c,address=0x48),ADS.ADS1115(i2c,address=0x49),ADS.ADS1115(i2c,address=0x4A)]

inputs0 = [AnalogIn(adc[0],ADS.P0),AnalogIn(adc[0],ADS.P1),AnalogIn(adc[0],ADS.P2),AnalogIn(adc[0],ADS.P3)]
inputs1 = [AnalogIn(adc[0],ADS.P0),AnalogIn(adc[0],ADS.P1),AnalogIn(adc[0],ADS.P2),AnalogIn(adc[0],ADS.P3)]
inputs2 = [AnalogIn(adc[0],ADS.P0),AnalogIn(adc[0],ADS.P1),AnalogIn(adc[0],ADS.P2),AnalogIn(adc[0],ADS.P3)]

norm = 4.95 # ADC voltage normalization value

def db_to_float(number):
	"""Converts dB to float values"""
	return(10**(number/20))


def float_to_db(number):
	# if ((number > 1) or (number < 0)):
		# print("value must be between 0 and 1 to convert to dB. Got ", number)
		# raise(ValueError)
	return(20*log10(number))


class joystick():
	def __init__(self):
		self.x = 0
		self.y = 0

class DSP():
	"""DSP class for writing to the DSP and keeping track of variable changes"""
	class I(): # Input object
		def __init__(self):
			self.name = 'placeholder'
			self.ind = -1 # Short for index
			self.gain = 0
			self.mute = True
			self.vol = self.gain*self.mute # TODO check that this gets updated
			#print(self,self.name)

		def __setattr__(self, name, value):
			"""This function is where callbacks are defined for variable changes"""
			if name == 'gain':
				self.set_gain(value)
			elif name == 'mute':
				self.set_mute(value)
			super().__setattr__(name, value)			
		
		def set_mute(self, status):
			print(self, 'set mute to ',status)
			# queue(status) # TODO proper format

		def set_gain(self, gain):
			print(self, 'set mute to ',gain)
			#queue(gain) # TODO proper format

	class O(): # Output object
		def __init__(self):
			self.name = 'placeholder'
			self.id = -1
			self.ind = -1
			self.delay = 0
			self.gain = 0
			self.mute = True
			self.HPF = False
			self.LPF = False # Alternative is cutoff frequency
			self.sources = (0,)*NUM_INPUTS # Sorry this had to be a tuple
			self.vol = self.gain*self.mute # TODO check that this gets updated
			#print(self,self.name)

		def __setattr__(self, name, value):
			"""This function is where callbacks are defined for variable changes"""
			if name == 'delay':
				self.set_delay(value)
			elif name == 'mute':
				self.set_mute(value)
			elif name == 'HPF':
				self.set_HPF(value)
			elif name == 'LPF':
				self.set_LPF(value)
			elif name == 'gain':
				self.set_gain(value)
			elif name == 'mute':
				self.set_mute(value)
			elif name == 'sources':
				self.set_sources(value)
			super().__setattr__(name, value)			

		def set_HPF(self, freq):
			if freq:				
				print(self, 'set HPF to ',freq,'Hz')
				#queue(freq) # TODO proper format
			else:
				print('HPF bypass')
				#queue('HPF bypass') # TODO proper format

		def set_LPF(self, freq):
			if freq:				
				print(self, 'set LPF to ',freq,'Hz')
				#queue(freq) # TODO proper format
			else:
				print('LPF bypass')
				#queue('LPF bypass') # TODO proper format

		def set_delay(self, delay):
			#print(self, 'set delay to ',delay)
			val = 0
			if (delay < 0):
					delay = 0
			if (delay > 80):
					delay = 80
			val = int(delay*48) # Convert to right value range for hex conversion
			# print('int: ',val)
			val = "{0:#0{1}x}".format(val,6) #
			# print("hex: ",val)
			val = val[2:] #strip 0x prefix
			cmd = [int(val[:2],16),int(val[2:4],16)]
			#print('set delay',val)
			queue([ADDR,0x04,[int(0xC4+self.ind),0x00,0x00]+cmd]) # TODO proper format

		def set_mute(self, status):
			#print(self, 'set mute to ',status)
			queue([ADDR,0x00,[int(hex(0x1E+(self.ind*3)),16),0X00, 0X00, 0X00, 0X00]])
			queue([ADDR,0x00,[0x1D,0x00, 0x00,0x20,0x8A]])

		def set_gain(self, gain):
			print(self, 'set gain to ',gain)
			#queue(gain) # TODO proper format



		def set_sources(self, gain_vals):
			"""Note, the entire list must be updated at once for the setattr
			to trigger. """
			val = 0 # variable initalization
			for i in range(len(gain_vals)):
				if gain_vals[i] != -1:#self.sources[i]: # Don't update if not needed
					#converts to, and returns 4 hex values
					# 0 is 0x00, 0x00, 0x00, 0x00, 0x00
					# 1 is 0x00, 0x01, 0x00, 0x00, 0x00
					# https://stackoverflow.com/questions/12638408/decorating-hex-function-to-pad-zeros
					# Range limit:
					val = gain_vals[i]
					if (val < 0):
							val = 0
					elif (val > 10): # Arbitrary, may be changed
							val = 10
					val = int(val*16777216) # Convert to right value range for hex conversion
					val = "{0:#0{1}x}".format(val,10) #
					val = val[2:] #strip 0x prefix
					ret = [int(val[:2],16),int(val[2:4],16),int(val[4:6],16),int(val[6:8],16)]
					queue([ADDR,0x60,[0x00]+ret]) # value
					#print("index/address value: ")
					#print(str(0x8C+i+0x04*self.ind))
					queue([ADDR,0x60,[0x05,0x00,0x00,0x01]+[0x8C+i+0x04*self.ind]+[0x00,0x00,0x00,0x01]]) # location

			#print(self, 'set sources to ',gain_vals)
			#print(commands)
			#queue(sources) # TODO proper format


	def __init__(self):
		self.name = 'test'
		self.input = []
		self.output = []
		for i in range(NUM_INPUTS):
			self.input.append(self.I())
			self.input[i].ind = i
			self.input[i].id = 'DSP.input['+str(i)+']'
			self.input[i].name = 'input '+str(i)
		for o in range(NUM_OUTPUTS):
			self.output.append(self.O())
			self.output[o].ind = o
			self.output[o].id = 'DSP.output['+str(o)+']'
			self.output[o].name = 'output '+str(o)


	def mute_all():
		print("stub to mute all")

	def unmute_all():
		print("stub to unmute all")

	def callback(self, value):
		print('callback, value ',value)

def queue(data):
	#print('queued ',data)
	"""data should be a list, with the following format:
	[i2c address, memory address, [data]]
	data should be less than 32 bytes at a time.
	This function might be unnecessary,
	you could just append to commands, but I think this is neater"""
	global commands
	commands.append(data)

def run_queue():
	global commands
	"""This function is to be run in a thread so I2C writes don't hang the
	main program / GUI or interfere with each other. 
	May need to compartmentalize to SPI and I2C"""
	while True:
		if commands:
			#print(commands.pop(0))
			#print('cmd: ',cmd)
			#sleep(0.01)
			X = commands.pop(0)
			#print('X: ',X)
			
			try:
				bus.write_i2c_block_data(X[0],X[1],X[2])
			except Exception as e:
				print("INVALID COMMAND!")
				print(e)
#				print("Command: ",X)
			#print('commands pop: ',commands.pop(0))
			#sleep(0.01)

queue_thread = Thread(target=run_queue, daemon=True)
queue_thread.start()

def read_controls():
	global slider, pot
	"""Stub function to read physical control inputs"""
	while True:
		for i in range(len(inputs0)): # Use ADC 0 for sliders
			slider[i] = inputs0[i].voltage/norm
		joystick.x = inputs1[0].voltage/norm # use ADC 1 for joystick
		joystick.y = inputs1[1].voltage/norm
		pot[0] = inputs2[0].voltage/norm # Use ADC 2 for rotary potentiometers
		pot[1] = inputs2[1].voltage/norm
		#print('read voltage',flush=True)

# Ref: https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15
# Analog controls that get read: 
# linear potentiometers (4x)
# rotary potentiometers (4x)
# Joystick (1x, 2 channels)
# This means that we can use 3 4 channel ADC's

ReadThread = Thread(target=read_controls)
ReadThread.daemon = True
ReadThread.start()

# Yes this overwrites a class, no I don't care.
# In fact I did it on purpose to reduce possibility of error.
DSP = DSP()

joystick = joystick()

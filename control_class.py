#!/usr/bin/env python3

# Notes on how docstrings should be implemented:
# https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
# Please try to generally adhere to PEP8 coding standards.
# Tkinter imports may be an exception
# Callback example: 
# https://stackoverflow.com/questions/51885246/callback-on-variable-change-in-python

#Imports
'''
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
'''
from time import sleep
from math import acos, asin, atan, atan2, ceil, cos, degrees, e, exp, floor
from math import gcd, log, log10, pow, sqrt, sin, tan, radians, pi, tau
from datetime import datetime
from threading import Thread

NUM_INPUTS = 4
NUM_OUTPUTS = 8
NUM_CONTROLS = 20

# Might want to move this to a dictionary for easier referencing
controls = [0]*NUM_CONTROLS

commands = [] # This is the global variable to store the command queue

def db_to_float(number):
	"""Converts dB to float values"""
	return(10**(number/20))


def float_to_db(number):
	# if ((number > 1) or (number < 0)):
		# print("value must be between 0 and 1 to convert to dB. Got ", number)
		# raise(ValueError)
	return(20*log10(number))


class DSP():
	"""DSP class for writing to the DSP and keeping track of variable changes"""
	class I(): # Input object
		def __init__(self):
			self.name = 'placeholder'
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
			#print(self, 'set mute to ',status)
			queue(status) # TODO proper format

		def set_gain(self, gain):
			#print(self, 'set mute to ',gain)
			queue(gain) # TODO proper format

	class O(): # Output object
		def __init__(self):
			self.name = 'placeholder'
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
				#print(self, 'set HPF to ',freq,'Hz')
				queue(freq) # TODO proper format
			else:
				#print('HPF bypass')
				queue('HPF bypass') # TODO proper format

		def set_LPF(self, freq):
			if freq:				
				#print(self, 'set LPF to ',freq,'Hz')
				queue(freq) # TODO proper format
			else:
				#print('LPF bypass')
				queue('LPF bypass') # TODO proper format

		def set_delay(self, delay):
			#print(self, 'set delay to ',delay)
			queue(delay) # TODO proper format

		def set_mute(self, status):
			#print(self, 'set mute to ',status)
			queue(status) # TODO proper format

		def set_gain(self, gain):
			#print(self, 'set gain to ',gain)
			queue(gain) # TODO proper format

		def set_sources(self, sources):
			"""Note, the entire list must be updated at once for the setattr
			to trigger. """
			#print(self, 'set sources to ',sources)
			queue(sources) # TODO proper format


	def __init__(self):
		self.name = 'test'
		self.input = []
		self.output = []
		for i in range(NUM_INPUTS):
			self.input.append(self.I())
			self.input[i].id = 'DSP.input['+str(i)+']'
			self.input[i].name = 'input '+str(i)
		for o in range(NUM_OUTPUTS):
			self.output.append(self.O())
			self.output[o].id = 'DSP.output['+str(o)+']'
			self.output[o].name = 'output '+str(o)


	def mute_all():
		print("stub to mute all")

	def unmute_all():
		print("stub to unmute all")

	def callback(self, value):
		print('callback, value ',value)


def queue(data):
	"""data should be a list, with the following format:
	[i2c address, memory address, [data]]
	data should be less than 32 bytes at a time.
	This function might be unnecessary,
	you could just append to commands, but I think this is neater"""
	global commands
	commands.append(data)

def run_queue():
	"""This function is to be run in a thread so I2C writes don't hang the
	main program / GUI or interfere with each other. 
	May need to compartmentalize to SPI and I2C"""
	while True:
		if commands:
			# Smbus block write goes here TODO
			print('queue: ',commands.pop(0))
			sleep(0.1)

queue_thread = Thread(target=run_queue, daemon=True)
queue_thread.start()

def read_controls():
	"""Stub function to read physical control inputs"""
	while True:
		# Read ADC. TODO
		sleep(1)

read_control_thread = Thread(target=read_controls, daemon = True)
read_control_thread.start()

# Yes this overwrites a class, no I don't care.
# In fact I did it on purpose to reduce possibility of error.
DSP = DSP()

# Ref: https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15
# Analog controls that get read: 
# linear potentiometers (4x)
# rotary potentiometers (4x)
# Joystick (1x, 2 channels)
# This means that we can use 3 4 channel ADC's

# Binary inputs (toggle switches, buttons, etc.)
# should be set up using interrupts. 
# Need to ensure that interrupts do not interfere with writes in progress

def read_control(control):
	global controls
	#Change to pinout control (sets analog control to read)
	mux_0 = control % 4
	mux_1 = control % 2
	mux_2 = control % 1
	
	result = 0 # TODO

def read_all():
	for i in range(len(controls)):
		controls[i] = read_control(i)


ReadThread = Thread(target=read_all)
ReadThread.daemon = True
ReadThread.start()

def run():
	while True:
		if len(controls) > 20: # Placeholder exception?
			print("too many control values added, exiting")
			raise RuntimeError
			
		for i in range(len(controls)):
			controls[i] = read_
		###
		# Section to execute user code
		###

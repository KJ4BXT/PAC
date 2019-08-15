#!/usr/bin/env python3

# Notes on how docstrings should be implemented:
# https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
# Please try to generally adhere to PEP8 coding standards.
# Tkinter imports may be an exception

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

def db_to_float(number):
	"""Converts """
	return(10**(number/20))


def float_to_db(number):
	if ((number > 1) or (number < 0)):
		print("value must be between 0 and 1 to convert to dB. Got ", number)
		raise(ValueError)
	return(20*log10(number))

# Need to figure out how / where to put DSP update hooks

class DSP():
	
	class I():
		def __init__(self,gain=0,mute=True):
			name = int(len(DSP.input)) + 1
			print(self,self.name)
		def mute():
			print(self,'muted input ',self.name)
			# SPI write command
		def set_gain(gain):
			print(self,'set input ',self.name,' gain to ',gain)
			# SPI write command
		def adjust_gain(incr):
			print(self,'adjusted input ',self.name,' to ',gain)
			# SPI write command

	class O(): # Output object
		def __init__(self):
			name = int(len(DSP.output)) + 1
			self.delay = 0
			self.gain = 0
			self.mute = True
			self.HPF = False
			self.LPF = False # Alternative is cutoff frequency
			self.vol = gain*mute # TODO check that this gets updated
			print(self,self.name)
		def mute():
			print(self, 'output muted')
		
		def set_HPF(freq):
			

	def __init__(self):
		self.input = []
		self.output = []
		for i in range(NUM_INPUTS):
			input.append(I())
		for o in range(NUM_OUTPUTS):
			output.append(O())
	
	def mute_all():
		print("stub to mute all")
	
	def unmute_all():
		print("stub to unmute all")

# Ref: https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15
# Analog controls that get read: 
# linear potentiometers (4x)
# rotary potentiometers (4x)
# Joystick (1x, 2 channels)
# This means that we can use 3 4 channel ADC's

# Binary inputs (toggle switches, buttons, etc.)
# should be set up using interrupts

def read_control(control):
	global controls
	#Change to pinout control (sets analog control to read)
	mux_0 = control % 4
	mux_1 = control % 2
	mux_2 = control % 1
	
	result = 

def read_all():
	for i in range(len(controls)):
		controls[i] = read_control(i)


ReadThread = Thread(target=read_all)
ReadThread.daemon = True
ReadThread.start()

def run():
	while True:
		if len(controls) > 20:
			print("too many control values added, exiting")
			raise RuntimeError
			
		for i in range(len(controls)):
			controls[i] = read_
		###
		# Section to execute user code
		###

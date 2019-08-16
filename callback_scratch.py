
NUM_INPUTS = 4
NUM_OUTPUTS = 0
NUM_CONTROLS = 20

class DSP:

	class I():
		def __init__(self,gain=0,mute=True):
			self._callbacks = [self.queue]
			#name = int(len(DSP.input)) + 1
			self.name = 'name all'
			self._gain = 0
			#print(self,self.name)
		def mute():
			print(self,'muted input ',self.name)
			# SPI write command
		def set_gain(gain):
			print(self,'set input ',self.name,' gain to ',gain)
			# SPI write command
		def adjust_gain(incr):
			print(self,'adjusted input ',self.name,' to ',gain)
			# SPI write command
		
		@property
		def gain(self):
			return self._gain

		@gain.setter
		def gain(self, new_value):
			old_value = self._gain
			self._gain = new_value
			self._notify_observers(old_value, new_value)

		def _notify_observers(self, old_value, new_value):
			for callback in self._callbacks:
				callback(old_value, new_value)

		def register_callback(self, callback):
			self._callbacks.append(callback)

		def queue(self, old_value, new_value):
			print("#"*40)
			print("#  ",old_value,"   ",new_value,"   #")
			print("#"*40)


	def __init__(self, initial_value=0):
		self._output = []
		self._input = []
		self._callbacks = [self.queue]
		
		for i in range(NUM_INPUTS):
			self._input.append(self.I())
		for o in range(NUM_OUTPUTS):
			self._output.append(self.O())


	@property
	def input(self):
		return self._input

	@input.setter
	def input(self, new_value):
		old_value = self._input
		self._input = new_value
		self._notify_observers(old_value, new_value)

	def _notify_observers(self, old_value, new_value):
		for callback in self._callbacks:
			callback(old_value, new_value)

	def register_callback(self, callback):
		self._callbacks.append(callback)

	def queue(self, old_value, new_value):
		print("#"*40)
		print("#  ",old_value,"   ",new_value,"   #")
		print("#"*40)
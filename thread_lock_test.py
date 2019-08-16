import threading
from time import sleep

threads = []

class test:
	def wait(self,t=1):
		sleep(t)
		print('ended')

T = test()

for i in range(10):
	threads.append(threading.Thread(target=T.wait, daemon=True))

print("Created list of threads, starting run")

for i in threads:
	i.start()
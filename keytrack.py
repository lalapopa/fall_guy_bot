import keyboard 
import time 
from datetime import datetime

file = open('keyLog.txt', 'w')
nowTime = datetime.now()

class keytrack:
	def __init__(self, keys):
		self.keys = keys
	def ispressed(self):
		results = []
		for key in self.keys:
			if keyboard.is_pressed(key):
				test1 = str('TIME = '+ (stopwatch_def.start())+ ' '+ key.upper() +'\n')
				results.append(test1)
		if len(results):
			return results
		else:
			return str('TIME = '+ (stopwatch_def.start())  + ' NOTHING'+'\n')
	def save_log(self, openedFile):
		whatKeyispressed = self.ispressed()
		for element in whatKeyispressed:
			openedFile.write(element)
		return stopwatch_def.start()

class stopwatch:
	def __init__(self,start_time):
		self.start_time = start_time
	
	def start(self):
		end_time = datetime.now()
		delta = str(end_time - self.start_time)   	#Result be like 'HH:MM:SS.MILLISECOND'(Millisecond have six numbers)
		trash = ':'		
		for char in trash: 
			delta = delta.replace(char,'')
		return delta.lstrip('0') 					#It's gonna be a string without zero's in middle 

stopwatch_def = stopwatch(nowTime)
keys = ['w','a','s','d','space','z']
kt = keytrack(keys)
while True:
	savekeylog = kt.save_log(file)
	print(savekeylog)
	time.sleep(0.01) 
	if keyboard.is_pressed('q'): 
		file.close()
		break 



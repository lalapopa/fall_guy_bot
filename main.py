import cv2 as cv
import numpy as np
import os
import time as tm 
from time import time
from datetime import datetime
import keyboard
from window_capture import WindowCapture
from level_detect import *
from data_path import *


class ImgSaver:
	def __init__(self, image_name, image, path):
		self.image_name = image_name
		self.image = image
		self.img_path = ['/IMG']

		for check_path in self.img_path:
			if os.path.exists(path + check_path):
				pass
			else:
				os.makedirs(path + check_path)
		self.path = path

	def write_in_path (self):
		os.chdir(self.path + self.img_path[0])
		cv.imwrite(self.image_name, self.image)


class LogMeneger:
	def __init__(self, path, create=''):
		self.path = path
		self.create = str('/')+create
		self.runLog_file = 'runLog.txt'
		self.keylog_file = 'keyLog.txt'

	def directory_crate(self):
		if os.path.exists(self.path + self.create):
			print('Directory exists')
			os.chdir(self.path + self.create)
			return self.path + self.create
		else:
			os.makedirs(self.path + self.create)
			os.chdir(self.path + self.create)
			return (self.path + self.create)


	def read_runlog(self):
		log_exists = os.path.isfile(self.runLog_file)
		if log_exists:
			file = open(self.runLog_file, 'r')
			runs_number = int(file.readline())
			return runs_number
		else:
			runs_number = 0
			file = open(self.runLog_file,'w')
			file.write(str(runs_number))
			file.close()
			return runs_number


	def save_runlog(self, runs_number):
		file = open(self.runLog_file,'w')
		file.write(str(runs_number))
		file.close()
		print('RUNS ' +str(runs_number)+' log saved')


	def read_keylog(self):
		try:
			return open(self.keylog_file, 'w')
		except Exception as e:
			print(e, 'No suck file')
			return []
			 

def vision_screencapture(wincap): 
	screenshot = wincap.get_screenshot()
	screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
	resize_screenshoot = cv.resize(screenshot, (427,240))
	resize_screenshoot = cv.adaptiveThreshold(resize_screenshoot,255,cv.ADAPTIVE_THRESH_MEAN_C,\
            cv.THRESH_BINARY,5,-5)
	cv.imshow('CV', resize_screenshoot)
	return resize_screenshoot


class KeyTracker:
	def __init__(self, keys):
		self.keys = keys
		self.start_time = datetime.now()


	def get_pressed_key_in_time(self):
		results = []
		for key in self.keys:
			if keyboard.is_pressed(key):
				text_log, pressing_time = self.__formatinglog(key)
				results.append(text_log)

		if len(results):
			return results, pressing_time
		else:
			return self.__formatinglog('NOTHING')


	def save_log_and_return_time(self, openedFile):
		whatKeyispressed, pressed_time = self.get_pressed_key_in_time()
		for element in whatKeyispressed:
			openedFile.write(element)
		return pressed_time


	def __formatinglog(self, name):
		press_time = self.get_time_for_log()
		text_for_log = str('TIME = '+ (press_time)+ ' '+ name.upper() +'\n')
		return text_for_log, press_time


	def get_time_for_log(self):
		end_time = datetime.now()
		delta = str(end_time - self.start_time)   	#Result be like 'HH:MM:SS.MILLISECOND'(Millisecond have six numbers)
		trash = ':'		
		for char in trash: 
			delta = delta.replace(char,'')
		return delta.lstrip('0') 					#It's gonna be a string without zero's in middle 


def recording_level(file_for_key_log, path_for_img_saving, keys_for_track):

	raw_screen = WindowCapture()
	loop_time = time()
	kt = KeyTracker(keys_for_track)

	run = False
	
	while not run:
		screen = vision_screencapture(raw_screen)
		run_time = kt.save_log_and_return_time(file_for_key_log)
		screen_name = get_screen_img_name(run_time) 

		save = ImgSaver(screen_name, screen, path_for_img_saving)
		save.write_in_path()

	    # debug the loop rate
		print('FPS {}'.format(1/(time() - loop_time)))
		loop_time = time()

		if keyboard.is_pressed('r'):
			cv.destroyAllWindows()
			file_for_key_log.close()
			break
				
		if cv.waitKey(1) == ord('r'):
			cv.destroyAllWindows()
			file_for_key_log.close()
			break


def get_screen_img_name(name): return '{}.jpg'.format(name) 


while(True):
	name_of_level = level_finder()
	directory_for_level = LogMeneger(path_data_levels, name_of_level)
	level_path = directory_for_level.directory_crate()
	number_of_runs = directory_for_level.read_runlog() + 1
	save_runs = directory_for_level.save_runlog(number_of_runs)

	directory_for_current_run = LogMeneger(level_path, str(number_of_runs))
	run_path = directory_for_current_run.directory_crate()

	key_log_file = directory_for_current_run.read_keylog()

	waiting_for_start()

	recording_level(key_log_file, run_path, keys)



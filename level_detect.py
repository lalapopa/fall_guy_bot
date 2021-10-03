import os 
import keyboard
import numpy as np
import cv2 as cv
from time import time, sleep
from window_capture import WindowCapture
from data_path import *

class LevelDetect:
	def __init__(self, path_to_img_folder, img_file_name):
		os.chdir(path_to_img_folder)

		self.readed_img = cv.imread(path_to_img_folder + '/{}.png'.format(img_file_name)) 

	def detection_img_on_screen(self, wincap):
		if self.readed_img is None:
			return False
		else:
			sc = wincap.get_screenshot()
			sc = cv.resize(sc, (1280,720))
			sc = cv.cvtColor(sc, cv.COLOR_BGR2GRAY)
			sc = sc.astype(np.uint8)

			img = self.readed_img
			img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
			img = img.astype(np.uint8)

			result = cv.matchTemplate(sc, img, cv.TM_CCOEFF_NORMED)
			min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
			trsh = 0.8
			if max_val >= trsh:
				return True
			else:
				return False


#Procceding img 
def level_finder():
	wincap = WindowCapture()
	service_buttons = (
		'finding_game', 
		'finding_game2', 
		'Youlost', 
		'nextlevel',
		)

	while True:
		for img in service_buttons:
			detector = LevelDetect(path_service,img)
			FindImgResult = detector.detection_img_on_screen(wincap)
			if FindImgResult:
				print('finding levels')
				level_find = False
				while not level_find:
					for level in levels:
						level_detector = LevelDetect(path_levels,level)
						level_find = level_detector.detection_img_on_screen(wincap)
						if level_find:
							print('i find ' + level)
							find_level = level
							return find_level


def waiting_for_start():
	wincap = WindowCapture()
	service_buttons = (
		'go',
		)
	print('Start finding GO img...')
	while True:
		for img in service_buttons:
			detector = LevelDetect(path_service,img)
			FindImgResult = detector.detection_img_on_screen(wincap)
			if FindImgResult:
				print('find GO img')
				return True


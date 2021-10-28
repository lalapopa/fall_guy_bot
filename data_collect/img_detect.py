import os 
import keyboard
import numpy as np
import cv2 as cv
import logging

from window_capture import WindowCapture
from service.service_data import ServiceData as sd

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
			min_val, max_val, _, _ = cv.minMaxLoc(result)
			trsh = 0.78

			if max_val >= trsh:
				return True
			else:
				return False


def level_finder():
	while True:
		if recognition(sd.service_buttons, sd.path_service):
			level_name = recognition(sd.levels, sd.path_levels)
			return level_name
			

def recognition(imgs, path_to_img):
	while True:
		for img in imgs:
			detector = LevelDetect(path_to_img, img)
			find_img = detector.detection_img_on_screen(WindowCapture())
			if find_img:
				logging.debug(f'I find {img!r}')
				return img


def go_text_finder():
	if recognition(sd.go_text, sd.path_service):
		return True



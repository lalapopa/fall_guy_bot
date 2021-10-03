import os
import cv2
import pickle
import pandas as pd
import numpy as np
from save_csv_log_in_runs import do_return_df_from_all_runs

def save(level, delete=False,debug=False):
	os.chdir("D:/Documents/Python/fallguy_bot/DATA/LEVELS/" + level)
	if delete is True:
		try:
			os.remove('X.pickle')
			os.remove('y.pickle')
		except FileNotFoundError:
			print('File to delete Not found')
			pass

	if os.path.isfile('./X.pickle') is True:
		print('Already saved')

	else:
		df = do_return_df_from_all_runs(level, debug)
		df = df.reset_index()
		del df['index']
		frame_df = df['Frame']
		categories_df = df['Categories']
		print('i found ',len(frame_df),' Data')
		training_data = []
		for img in range(len(frame_df)):
			training_data.append([frame_df[img], categories_df[img]])

		X = []
		y = []
		IMG_SIZE_X = 427
		IMG_SIZE_Y = 240

		for features, label in training_data:
			X.append(features)
			y.append(label)
		X = np.array(X).reshape(-1, IMG_SIZE_X, IMG_SIZE_Y, 1)
		y = np.array(y)
		os.chdir("D:/Documents/Python/fallguy_bot/DATA/LEVELS/" + level)
		save_pickle_file(X, y)


def save_pickle_file(X, y):
	print('Saving to pickle in '+ os.getcwd())

	pickle_out = open("X.pickle","wb") #Our IMGs
	pickle.dump(X, pickle_out)
	pickle_out.close()
	pickle_out = open("y.pickle","wb") #Our Lable
	pickle.dump(y, pickle_out)
	pickle_out.close()
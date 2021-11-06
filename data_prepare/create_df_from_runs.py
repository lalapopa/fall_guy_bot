import os 
import cv2
import pandas as pd
import numpy as np 
from .key_log_handler import get_time_and_keys 
from service.service_data import ServiceData as sd


def return_df_from_all_runs(level, debug=False):
	path = append_path(sd.path_data_levels, adding=level)

	if os.path.exists(path):
		print('Reading:',path)
		runs_number = read_run_log(path)
		df2 = pd.DataFrame()

		for run in range(1, runs_number+1):
			if change_dir(path, run): 
				key_log = read_key_log()
				time, categories = get_time_and_keys(key_log)
				images_list, dead_pos = read_imgs_in_run(time)
				if not images_list: continue 

				fine_categories = remove_dead_categories(categories, dead_pos)
				debug_log(run, 
					dead_pos, 
					categories,
					fine_categories, 
					time, 
					images_list, 
					debug)

				df = make_dataframe_from_img_and_categories(images_list, fine_categories)
				df2 = join_dataframe(df,df2)

	else:
		print('Directory not found',path)
		return False
	return df2


def append_path(path, adding=''):
	return os.path.join(path, adding).replace('\\','/')

def read_run_log(path_level):
	try:
		os.chdir(path_level)
	except Exception as e:
		print(f'No directory with name: {path_level}\n{e}')
		return False
		
	run_log_name = 'runLog.txt'
	try:
		with open(run_log_name) as f:
			return int(f.readline())
	except FileNotFoundError as e:
		print(f'In {path_level} no runLog.txt\n{e}')
		return False

def change_dir(path,folder_name):
	try:
		os.chdir(append_path(path, adding=str(folder_name)))
		return True
	except Exception as e:
		print(e)
		return False



	
def read_key_log():
	log_name = 'keyLog.txt'
	log = open(log_name, 'r', encoding='utf-8')
	return log


def read_imgs_in_run(name_list):
	path = os.getcwd()
	try:
		os.chdir(path + '/IMG')
	except FileNotFoundError:
		print(f'No image in : {path}')
		return False, False

	img_list = []
	readed_img_list = get_all_img_names()
	dead_pos = []

	for i, name in enumerate(name_list):
		if float(name) in readed_img_list:
			img_name = name + '.jpg'
			img = read_img(img_name)
			img = crop_img(img) 
			img = resize_img(img)
			img_list.append(img)
		else:
			dead_pos.append(i)

	return img_list, dead_pos

def get_all_img_names():
	raw_img_names = os.listdir()
	img_name = [float(name[:-4]) for name in raw_img_names]
	img_name.sort()
	return img_name



def read_img(file_name):
	try:
		img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
		return img
	except FileNotFoundError:
		print(f'cant read {name} img')
	

def resize_img(img):
	try:
		img = cv2.resize(img, (sd.img_size_x, sd.img_size_y))
		# (_, gray_img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
		return img
	except Exception as e:
		pass 


def crop_img(img):
	# remove gui from left and right side with timer and task  
	return img[:, 71:372]


def remove_dead_categories(array, pos):
	raw_array = [val for val in array]

	for i in pos[::-1]:
		raw_array.pop(i)
	return raw_array


def make_dataframe_from_img_and_categories(images, array):

	data = {'Frame': [],
		'Categories':[],
	   }

	for index, image in enumerate(images):
		data['Frame'].append(image)
		data['Categories'].append(array[index])

	df = pd.DataFrame(data)

	return df

def join_dataframe(df, df2):
	if df2 is None:
		return df
	else:
		df = pd.concat([df,df2])
		return df

def debug_log(run, rp, c, nc, il, ilwn,Show=True):
	if Show is True:
		print('Run #', run)
		print('Dead categories=', len(rp))
		print('Raw  categories=', len(c))
		print('Fine categories=', len(nc))
		print('Raw  img list=', len(il))
		print('Fine img list=', len(ilwn))

if __name__ == '__main__':
	main()
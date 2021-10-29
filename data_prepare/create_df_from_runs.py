import os 
import cv2
import pandas as pd
import numpy as np 
from .key_log_handler import return_time_key_from_log as get_time_and_keys
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

				images_list = read_imgs_in_run(time)
				if not images_list: continue 
				images_list_without_none, removed_position = remove_none_from_img_array(images_list)
				normalized_categories = allign_categories_array_with_img_array(categories, removed_position)

				debug_log(run,removed_position, normalized_categories, categories, images_list, images_list_without_none, debug)

				df = make_dataframe_from_img_and_categories(images_list_without_none, normalized_categories)
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
		return False

	img_list = []

	for name in name_list:
		img_name = name + '.jpg'
		img = read_img(img_name)
		img = resize_img(img)	

		img_list.append(img)

	return img_list

def read_img(file_name):
	try:
		img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
		return img
	except FileNotFoundError:
		print(f'cant read {name} img')
	

def resize_img(img):
	try:
		img = cv2.resize(img, (sd.img_size_x, sd.img_size_y))
		(thresh, gray_img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
		return gray_img
	except Exception as e:
		pass 


def remove_none_from_img_array(img_array):
	none_positions = []
	counter = -1 
	raw_img_array = [img for img in img_array]
	
	for img in img_array:
		counter += 1
		if img is None:
			none_positions.append(counter)
			
	none_positions.sort(reverse=True)
	
	for position in none_positions:
		raw_img_array.pop(position)
		
	return raw_img_array, none_positions


def allign_categories_array_with_img_array(categories_array, remove_position):
	cleaned_categories_array = [num for num in categories_array]
	
	for position in remove_position:
		cleaned_categories_array.pop(position)
		
	return cleaned_categories_array

def find_usage_key(category_list, finding_key):

	finding_key = sd.keys_categories[finding_key]
	positions = []

	for num in finding_key:
		if num == 1:
			target_position = finding_key.index(num)

	counter = -1 
	counter2 = -1 

	for category in category_list:
		counter2 += 1
		for num in category:
			counter += 1
			if counter == target_position and num == 1:
				positions.append(counter2)
		counter = -1
	return positions


def make_dataframe_from_img_and_categories(images, categories):

	data = {'Frame': [],
		'Categories':[],
	   }

	counter = -1 
	for image in images:
		counter += 1
		data['Frame'].append(image)
		data['Categories'].append(categories[counter])

	df = pd.DataFrame(data)

	return df

def join_dataframe(df, df2):
	if df2 is None:
		return df
	else:
		df = pd.concat([df,df2])
		return df

def debug_log(run,rp,nc,c,il,ilwn,Show=True):
	if Show is True:
		print('Run #', run)
		print('Dead categories=', len(rp))
		print('Fine categories=', len(nc))
		print('Raw  categories=', len(c))
		print('raw  img list=', len(il))
		print('Fine img list=', len(ilwn))

if __name__ == '__main__':
	main()
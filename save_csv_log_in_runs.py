import os 
import cv2
import pandas as pd
import numpy as np 
from key_log_handler import getTimeAndKeyFromKeylog as getTimeAndKey


def do_return_df_from_all_runs(level, debug=False):
	path = 'D:/Documents/Python/fallguy_bot/DATA/LEVELS'
	path = appendPath(path, adding=level)

	if os.path.exists(path):
		print('Reading:',path)
		NumberOfRuns = ReadRunsLogFromLevelPath(path)
		df2 = pd.DataFrame()
		for Run in range(1,NumberOfRuns+1):
			if not ChangeDirForRun(path, Run): continue
			key_log = ReadKeyLogFromLevel()
			time, categories = getTimeAndKey(key_log)
			images_list = ReadIMGFromLevel(time)
			images_list_without_none, removed_position = remove_none_from_img_array(images_list)
			normalized_categories = allign_categories_array_with_img_array(categories, removed_position)
			debug_log(Run,removed_position, normalized_categories, categories, images_list, images_list_without_none, debug)
			df = make_dataframe_from_img_and_categories(images_list_without_none, normalized_categories)
			df2 = join_dataframe(df,df2)
	else:
		print('Directory not found',path)
	return df2

def appendPath(path, adding=''):
    path = path + '/' + adding
    return path


def ReadRunsLogFromLevelPath(LevelPath):
    try:
        os.chdir(LevelPath)
    except Exception as e:
        print(e)
        pass
    
    LogName = 'runLog.txt'
    LogExists = os.path.isfile(LogName)
    try:
        if LogExists:
            OpenLog = open(LogName, 'r')
            RunsNumber = int(OpenLog.readline())
            return RunsNumber
        else:
            Print('log in' + str(LevelPath) +'Doesnt exist')
    except Exception as e:
        pass
    

def ChangeDirForRun(path,folder_name):
    try:
        os.chdir(appendPath(path, adding=str(folder_name)))
        return True
    except Exception as e:
        print(e)
        return False
            
    
def ReadKeyLogFromLevel():
    LogName = 'keyLog.txt'
    Log = open(LogName, 'r', encoding='utf-8')
    return Log


def ReadIMGFromLevel(name_list):
	path = os.getcwd()
	os.chdir(path + '/IMG')

	img_list = []
	for name in name_list:
		try: 
			file = name + '.jpg'
			img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
			img_list.append(img)

		except Exception as e:
			pass
	return img_list


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
    keys_categories = {
    'W':        [1,0,0,0,0,0,0],
    'A':        [0,1,0,0,0,0,0],
    'S':        [0,0,1,0,0,0,0],
    'D':        [0,0,0,1,0,0,0],
    'SPACE':    [0,0,0,0,1,0,0],
    'E':        [0,0,0,0,0,1,0],
    'SHIFT':    [0,0,0,0,0,0,1],
    'NOTHING':  [0,0,0,0,0,0,0],
    } 

    finding_key = keys_categories[finding_key]
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
		image = np.array(image)
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


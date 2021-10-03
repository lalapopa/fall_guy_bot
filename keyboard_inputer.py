import keyboard
import time
import numpy as np

def return_key_from_categories(categories):
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
	position_of_one = find_one_in_array(categories)
	keys_list = [*keys_categories]
	keys = [] 

	if len(position_of_one) == 0:
		keys.append(keys_list[-1])
		return keys
	
	
	for key in keys_list:
		category = keys_categories.get(key)
		counter = -1 
		for num in category:
			counter += 1
			if num == 1 and counter in position_of_one:
				keys.append(key)

	return keys

def find_one_in_array(array):
	position = []
	count = -1
	threshold = 0.65
	for num in array:
		count += 1
		if num >= threshold:
			position.append(count)

	return position

def keyboard_input(keys,key_release):

	if key_release:
		for key in key_release:
			keyboard.send(key.lower(), do_press=False, do_release=True)

	if 'NOTHING' in keys:
		return []
	for key in keys:
		keyboard.send(key.lower(), do_release=False)
	return keys



def run_input(category, last_key=[]):
	category = category.tolist()
	keys = return_key_from_categories(category)
	print(keys)
	last_key = keyboard_input(keys, last_key)
	return last_key


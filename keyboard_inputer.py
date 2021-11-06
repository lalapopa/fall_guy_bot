import keyboard
from service.service_data import ServiceData as sd


def return_key_from_categories(categories):

	position_of_one = find_one_in_array(categories)
	keys_list = [*sd.keys_categories][1:] #except W
	keys = [] 

	if len(position_of_one) == 0:
		keys.append(keys_list[-1])
		return keys
	
	
	for key in keys_list:
		category = sd.keys_categories.get(key)
		counter = -1 
		for num in category[1:]:
			counter += 1
			if num == 1 and counter in position_of_one:
				keys.append(key)

	return keys

def find_one_in_array(array):
	position = []
	count = -1
	threshold = 0.5
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
	keyboard.send('w', do_release=False)

	category = category.tolist()	
	keys = return_key_from_categories(category)
	print(f'I pressing {keys}')
	# last_key = keyboard_input(keys, last_key)
	return last_key


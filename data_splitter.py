import random 
import numpy as np 


def get_train_and_test_data(X_array, y_array, data_percent=0.1):
	X_array.astype(np.float32)
	max_index = get_array_len(X_array)
	print('get max index')
	list_size_for_test = int(max_index*data_percent)
	index_for_test = get_unique_random_list(list_size_for_test, max_index)
	print('get index for test')

	print('getting index for train')
	
	index_for_train = get_list_without_given_element(max_index, index_for_test)

	print('creating X_test')
	X_test = np.stack([X_array[num] for num in index_for_test])
	print('creating y test')
	y_test = np.stack([y_array[num] for num in index_for_test])
	print('creating X_train')
	X_train = np.stack([X_array[num] for num in index_for_train])
	print('creating y_train')
	y_train = np.stack([y_array[num] for num in index_for_train])
	print('try to return')
	return X_train, y_train, X_test, y_test


def get_array_len(array):
	shape = np.shape(array)
	shape_in_list = list(shape)
	return shape_in_list[0]


def get_unique_random_list(list_len, max_number):
	random_list = []
	random_number = get_random_number(max_number)
	counter = 0
	for i in range(0,list_len):

		while check_for_duplicate(random_list, random_number):
			random_number = get_random_number(max_number)
			
			if counter >= max_number+1000:
				print('Cant create unique array with that array len. Max number should be = or > list len')
				return []
			else:
				counter += 1

		counter = 0

		random_list.append(random_number)

	return random_list


def get_random_number(max_number):
	return random.randint(0, max_number)


def check_for_duplicate(array, num):
	array_in_tuple = tuple(array)
	new_array = array_in_tuple + (num,)

	array_to_set = set(new_array)

	return not len(array_in_tuple) != len(array_to_set)


def get_list_without_given_element(array_size, element_positions):
	array = [num for num in range(0,array_size)]
	pos_to_delete = tuple(element_positions)
	for i in pos_to_delete:
		array.remove(i)
	return array


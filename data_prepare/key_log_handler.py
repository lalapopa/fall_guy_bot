from service.service_data import ServiceData as sd
import re

def get_time_and_keys(key_log):
	time = []
	keys = []

	for line in key_log:
		time.append(get_time(line))
		keys.append(get_keys(line, time[len(time)-1]))
	time_without_duplicates, duplicate_pos = kill_duplicates(time)
	keys_without_duplicates = merge_list_in_positions(keys, duplicate_pos)
	keys_categories = return_categories_from_key_list(keys_without_duplicates)
    
	return time_without_duplicates, keys_categories


def get_time(string):
    num = re.findall(r"\d+\.\d+|\d+|\.\d+", string)
    return num[0] #Re return our number in list so we need take first one 


def get_keys(string, time):
    trash_symb = 'TIME = ' + time + ' '
    if string.startswith(trash_symb):
        Key = string.replace(trash_symb, '', 1)
        Key = Key[:-1] # Remove new line \n symbols 
    return Key


def kill_duplicates(seq):
    seen = {}
    dup_pos = []
    dup_pair = []
    for index, item in enumerate(seq): 
        if item in seen: 
            dup_pair.append(index)
            if index == len(seq)-1:
                dup_pos.append(dup_pair)
            continue 

        seen[item] = 1
        if len(dup_pair) <= 1:
            dup_pair = [index,]
        if len(dup_pair) >= 2:
            dup_pos.append(dup_pair)
            dup_pair = [index,]

    return list(seen.keys()), dup_pos


def merge_list_in_positions(array, pos):
    ready_pair = []
    first_pos = []
    merged_list = []
    flat_pos = []

    for pair in pos:
        merged = []
        first_pos.append(pair[0])
        for i in pair:
            merged.append(array[i])
            flat_pos.append(i)
        ready_pair.append(merged)

    for i, val in enumerate(array):
        if i in first_pos:
            merged_list.append(ready_pair[first_pos.index(i)])
        if i in flat_pos:
            continue

        merged_list.append(val)
    return merged_list

def return_categories_from_key_list(key_list):
 
    category_list = []

    for keys in key_list:
        if type(keys) is str:
            category_list.append(sd.keys_categories[keys])
        if type(keys) is list:
            category_list.append(connection_categories(keys))
    return category_list


def connection_categories(keys):
    need_categories = []
    for key in keys:
        need_categories.append(sd.keys_categories[key])

    valid_pos = [] 
    for arr in need_categories:
        for i, val in enumerate(arr):
            if val:
                valid_pos.append(i)

    valid_categories = []
    for i, val in enumerate(need_categories[0]):
        if i in valid_pos:
            valid_categories.append(1)
        else:
            valid_categories.append(0)

    return valid_categories

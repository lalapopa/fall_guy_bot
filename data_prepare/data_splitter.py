import random 
import numpy as np 
from service.service_data import ServiceData as sd

def get_train_and_test_data(X_array, y_array, data_percent=0.1):

    y_normalized, taken_position = normalize_data(y_array)
    X_normalized = [X_array[pos] for pos in taken_position]

    max_index = get_img_amount(X_normalized) - 1  #we need last index available 

    print(max_index)

    list_size_for_test = int(max_index*data_percent)

    index_for_test = get_unique_random_list(list_size_for_test, max_index)
    index_for_train = get_list_without_given_element(max_index, index_for_test)

    print('creating X_test')
    X_test = np.stack([X_normalized[num] for num in index_for_test])

    print('creating y test')
    y_test = np.stack([y_normalized[num] for num in index_for_test])

    print('creating X_train')
    X_train = np.stack([X_normalized[num] for num in index_for_train])

    print('creating y_train')
    y_train = np.stack([y_normalized[num] for num in index_for_train])

    print('try to return')
    return X_train, y_train, X_test, y_test

def normalize_data(y_array):
    key_pos = [0, 1, 2, 3, 4, 5]  # 0 - W; 1 - A; 2 - S; 3 - D; 4 - SPACE;
    press_dict = {
    'W_nums': 0,
    'A_nums': 0,
    'S_nums': 0,
    'D_nums': 0,
    'SPACE_nums': 0,
    'E_nums': 0,
    }

    pos_in_y = {
    'W_nums': [],
    'A_nums': [],
    'S_nums': [],
    'D_nums': [],
    'SPACE_nums': [],
    'E_nums': [],
    }
    for lable_index, label in enumerate(y_array):
        for index, num in enumerate(label):
            if num == 1 and index in key_pos:
                if index == key_pos[0]:
                    press_dict['W_nums'] += 1
                    pos_in_y['W_nums'].append(lable_index)
                if index == key_pos[1]:
                    press_dict['A_nums'] += 1
                    pos_in_y['A_nums'].append(lable_index)
                if index == key_pos[2]:
                    press_dict['S_nums'] += 1
                    pos_in_y['S_nums'].append(lable_index)
                if index == key_pos[3]:
                    press_dict['D_nums'] += 1
                    pos_in_y['D_nums'].append(lable_index)
                if index == key_pos[4]:
                    press_dict['SPACE_nums'] += 1
                    pos_in_y['SPACE_nums'].append(lable_index)
                if index == key_pos[5]:
                    press_dict['E_nums'] += 1
                    pos_in_y['E_nums'].append(lable_index)

    # press_amount = sum(press_dict.values())
    # avg_press = int(press_amount/len(press_dict))
  
    max_value = max(press_dict.values())
    print(f'press_number in key = {press_dict}')
    print(f'max press = {max_value}')
    new_pos_y = {}

    for key_name, value in pos_in_y.items():
        new_pos_y[key_name] = []
        if len(value) != 0:
            if len(value) < max_value:
                while max_value > len(new_pos_y[key_name]):
                    for i in value:
                        new_pos_y[key_name].append(i)
                        if len(new_pos_y[key_name]) >= max_value:
                            break

            if len(value) >= max_value:
                for_shuffle = [i for i in value]
                random.shuffle(for_shuffle)
                new_pos_y[key_name] = for_shuffle[:max_value]

    y_new = []
    positions = []

    #we take all key except 'W'
    new_pos_y = dict(list(new_pos_y.items())[1:]) #Removing W from dict
    for key, value in new_pos_y.items():
        print(f'In Key = {key}, press len list = {len(value)}')
        for pos in value:
            y_new.append(y_array[pos][1:]) #Removing W in list now index 0 is A key
            positions.append(pos)

    return y_new, positions



def get_img_amount(array):
    shape = np.shape(array)
    shape_in_list = list(shape)
    return shape_in_list[0]


def get_unique_random_list(list_len, max_number):
    return random.sample(range(0, max_number), list_len)


def get_list_without_given_element(array_size, element_positions):
    array = [num for num in range(0,array_size)]
    pos_to_delete = tuple(element_positions)
    for i in pos_to_delete:
        array.remove(i)
    return array

if __name__ == '__main__':
    print(get_unique_random_list(3, 5))
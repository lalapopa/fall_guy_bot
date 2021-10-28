import os
import cv2
import pandas as pd
import numpy as np

from .create_df_from_runs import return_df_from_all_runs
from service.service_data import ServiceData as sd

def save(level, delete=False,debug=False):
    os.chdir(os.path.join(sd.path_data_levels, level))
    if delete:
        try_delete()

    if os.path.isfile('./X.npy'):
        print('Already saved')
    else:
        df = return_df_from_all_runs(level, debug)
        df = df.reset_index()
        del df['index']
        frame_df = df['Frame']
        categories_df = df['Categories']

        print('i found ',len(frame_df),' Data')
        print(f'and {len(categories_df)} numbers of Categories')

        training_data = []
        for img in range(len(frame_df)):
            training_data.append([frame_df[img], categories_df[img]])

        X = []
        y = []


        for features, label in training_data:
            X.append(features)
            y.append(label)
            
        X = np.array(X).reshape(-1, 240, 427, 1) #Keras take 3 dimensional array 
        y = np.array(y)

        os.chdir("D:/Documents/Python/fallguy_bot/DATA/LEVELS/" + level)
        save_npy_file(X, y)

def try_delete():
    try:
        os.remove('X.npy')
        os.remove('y.npy')
    except FileNotFoundError:
        print('File to delete Not found')
        pass

def save_npy_file(X, y):
    print('Saving to Numpy in '+ os.getcwd())

    with open('X.npy', 'wb') as f:
        np.save(f, X)
    with open('y.npy', 'wb') as f:
        np.save(f, y)
  
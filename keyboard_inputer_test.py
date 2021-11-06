import os 
import numpy as np
import cv2
from data_prepare.save_data import save
from data_prepare.create_df_from_runs import return_df_from_all_runs


def read_file(file_name):
    with open(file_name, 'rb') as f:
        return np.load(f)


path = 'D:/Documents/Python/fallguy_bot/DATA/LEVELS/SnowballSurvival/1/IMG'

save('SnowballSurvival', delete=True, debug=True)

X = read_file('X.npy')
y = read_file('y.npy')
print(f'Data size = {len(X)}')
for i, img in enumerate(X):
	print(y[i])
	print(np.amax(img))
	print(img.dtype)
	print(img.shape)
	cv2.imshow('hey', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

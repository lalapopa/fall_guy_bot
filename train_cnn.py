import os 
import time 
import random
import numpy as np 
import cv2

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.layers.normalization import BatchNormalization
from keras.regularizers import l2
from tensorflow.keras.callbacks import TensorBoard
from keras.layers import MaxPool2D

from data_prepare.save_data import save
from data_prepare.data_splitter import get_train_and_test_data as gttd
from service.service_data import ServiceData as sd


def main():
    levels = sd.levels
    for level in levels:
        print(level)
        X, y = load_level(level)
        # X_train, y_train, X_test, y_test = gttd(X, y)
        # del X, y 
        # X_train, y_train, X_test, y_test = prepare_date(X_train, y_train, X_test, y_test)
        # cnn = CNN_model(X_train, y_train)
        # train_save_model(cnn, X_train, y_train, X_test, y_test, f'cnn_{level}')



def load_level(level):
    save(level, delete=True, debug=True)
    os.chdir('D:/Documents/Python/fallguy_bot/DATA/LEVELS/'+ level)
    X = read_file('X.npy')
    y = read_file('y.npy')
    return X, y


def read_file(file_name):
    with open(file_name, 'rb') as f:
        return np.load(f)


def prepare_date(X_train, y_train, X_test, y_test):
    X_train = X_train/255.0
    X_test = X_test/255.0

    y_train = np.asarray(y_train).astype('float32')
    y_test = np.asarray(y_test).astype('float32')

    return X_train, y_train, X_test, y_test


def CNN_model(X_train, y_train):
    model = Sequential()
    # 1st Convolutional Layer
    model.add(Conv2D(filters=96, input_shape=X_train.shape[1:], kernel_size=(11,11),\
     strides=(4,4), padding='valid'))
    model.add(Activation('relu'))
    # Pooling 
    model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2), padding='valid'))
    # Batch Normalisation before passing it to the next layer
    model.add(BatchNormalization())
    # 2nd Convolutional Layer
    model.add(Conv2D(filters=256, kernel_size=(5,5), strides=(1,1), padding='same'))
    model.add(Activation('relu'))
    # Pooling
    model.add(MaxPooling2D(pool_size=(3,3), strides=(2,2), padding='valid'))
    # Batch Normalisation
    model.add(BatchNormalization())
    # 3rd Convolutional Layer
    model.add(Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), padding='same'))
    model.add(Activation('relu'))
    # Batch Normalisation
    model.add(BatchNormalization())
    # 4th Convolutional Layer
    model.add(Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), padding='same'))
    model.add(Activation('relu'))
    # Batch Normalisation
    model.add(BatchNormalization())
    # 5th Convolutional Layer
    model.add(Conv2D(filters=256, kernel_size=(3,3), strides=(1,1), padding='same'))
    model.add(Activation('relu'))
    # Pooling
    model.add(MaxPooling2D(pool_size=(3,3), strides=(2,2), padding='valid'))
    # Batch Normalisation
    model.add(BatchNormalization())
    # Passing it to a dense layer
    model.add(Flatten())
    # 1st Dense Layer
    model.add(Dense(4096, input_shape=X_train.shape[1:]))
    model.add(Activation('relu'))
    # Add Dropout to prevent overfitting
    model.add(Dropout(0.4))
    # Batch Normalisation
    model.add(BatchNormalization())
    # 2nd Dense Layer
    model.add(Dense(4096))
    model.add(Activation('relu'))
    # Add Dropout
    model.add(Dropout(0.4))
    # Batch Normalisation
    model.add(BatchNormalization())
    #  output Layer 
    model.add(Dense(len(y_train[0])))
    model.add(Activation('sigmoid'))

    model.compile(
        loss="binary_crossentropy",
        optimizer='adam',
        metrics=['accuracy']
    )
    model.summary()
    
    return model


def train_save_model(model, X_train, y_train, X_test, y_test, name):
    NAME = 'CNN-{}'.format(int(time.time()))
    tensorboard = TensorBoard(log_dir='logs/{}'.format(NAME))

    model.fit(X_train, y_train, 
        batch_size=128, epochs=10, 
        validation_data=(X_test, y_test), 
        callbacks=[tensorboard],
        )

    model.save(f'{name}.model')

if __name__ == '__main__':
    main()
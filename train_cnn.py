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

from data_prepare.save_data import save
from data_prepare.data_splitter import get_train_and_test_data as gttd
from service.service_data import ServiceData as sd


def main():
    levels = sd.levels
    for level in levels[7:]:
        print(level)
        X, y = load_level(level)
        X_train, y_train, X_test, y_test = gttd(X, y)
        del X, y 
        X_train, y_train, X_test, y_test = prepare_date(X_train, y_train, X_test, y_test)
        cnn = CNN_model(X_train, y_train)
        train_save_model(cnn, X_train, y_train, X_test, y_test, f'cnn_{level}')



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

    # 2 sets of CRP (Convolution, RELU, Pooling)
    model.add(Conv2D(20, (5, 5), padding="same",
        input_shape=X_train.shape[1:], kernel_regularizer=l2(0.)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

    model.add(Conv2D(50, (5, 5), padding="same",
        kernel_regularizer=l2(0.)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

    # Fully connected layers (w/ RELU)
    model.add(Flatten())
    model.add(Dense(500, kernel_regularizer=l2(0.)))
    model.add(Activation("relu"))

    # Softmax (for classification)
    model.add(Dense(len(y_train[0]), kernel_regularizer=l2(0.)))
    model.add(Activation("softmax"))

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
        batch_size=64, epochs=5, 
        validation_data=(X_test, y_test), 
        callbacks=[tensorboard],
        )

    model.save(f'{name}.model')

if __name__ == '__main__':
    main()
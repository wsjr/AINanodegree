import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Activation
import keras
import string

# DONE: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    # containers for input/output pairs
    X = []
    y = []

    start_index = 0
    end_index = start_index + window_size
    while end_index < len(series):
        X.append(series[start_index:end_index])
        # Updated the indices
        start_index = start_index + 1
        end_index = start_index + window_size
        #end_index = end_index + 1
        #start_index = start_index + 1
    y = series[window_size:]
    
    # reshape each 
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)
    
    return X,y

# DONE: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(window_size):
    model = Sequential()
    model.add(LSTM(5, input_shape=(window_size, 1)))
    model.add(Dense(1))
    return model


### DONE: return the text input with only ascii lowercase and the punctuation given below included.
def cleaned_text(text):
    punctuation = ['!', ',', '.', ':', ';', '?']
    validchars = string.ascii_lowercase + ' ' + ''.join(punctuation)
    
    text_list = list(text)
    for i, c in enumerate(text_list):
        # Replace with empty space if its not ascii or valid punctuation.
        if c not in validchars:
            text_list[i] = ' '
    text = ''.join(text_list)

    return text

### DONE: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []

    start_index = 0
    end_index = start_index + window_size
    while end_index < len(text):
        # Populate the inputs and outputs based from the indices.
        inputs.append(text[start_index:end_index])
        outputs.append(text[end_index])
        # Move the start and end indices
        end_index = end_index + step_size
        start_index = start_index + step_size
    
    return inputs,outputs

# DONE: build the required RNN model: 
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
def build_part2_RNN(window_size, num_chars):
    model = Sequential()
    model.add(LSTM(200, input_shape=(window_size, num_chars)))
    model.add(Dense(num_chars))
    model.add(Activation('softmax'))
    return model

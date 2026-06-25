import tensorflow as tf
from tensorflow.keras.layers import Layer, Dense, Flatten, Reshape, Add, LayerNormalization, Dropout, Lambda, BatchNormalization, Embedding, Conv1D, LeakyReLU, Input, MultiHeadAttention, Add, GroupNormalization
import tensorflow as tf
import keras
from keras import layers
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Flatten, Reshape, Add, LayerNormalization, Dropout, Lambda, BatchNormalization, Embedding
from tensorflow.keras.layers import LSTM, SimpleRNN, GRU
from tensorflow.keras.layers import MaxPooling1D, MaxPool1D, Conv1D, Conv2D, MaxPooling2D, GlobalMaxPooling1D, GlobalAveragePooling1D, AveragePooling1D
from tensorflow.keras.layers import Activation, ELU, LeakyReLU, ReLU, PReLU
from tensorflow.keras.initializers import HeNormal, Constant
from tensorflow.keras import Input
from tensorflow.keras.callbacks import *
from keras.optimizers import Adam, RMSprop, SGD, AdamW, Adadelta, Adagrad, Adamax, Adafactor, Nadam, Ftrl, Lion, LossScaleOptimizer
from keras.applications import *
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras import backend as K
from keras.src import backend
from tensorflow.keras.losses import *
from keras.src import ops
from keras.src.losses.loss import squeeze_or_expand_to_same_rank
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import uuid



def CNN(trainX=None, testX=None, predX=None, trainY=None, testY=None):
    dim = len(trainY[0])
    inputs = Input(shape=(trainX[0].shape), name='x')
    use1d = len(inputs.shape) < 4
    outputs = Conv1D(filters=dim, kernel_size=1, activation=PReLU())(inputs) if use1d else Conv2D(filters=dim, kernel_size=(1,1),strides=(1,1), activation=PReLU())(inputs)
    #outputs = GroupNormalization(groups=64)(outputs)
    #outputs = Dropout(0.1)(outputs)
    outputs = Conv1D(filters=dim, kernel_size=1, activation=PReLU())(outputs) if use1d else Conv2D(filters=dim, kernel_size=(1,1),strides=(1,1), activation=PReLU())(outputs)
    #outputs = GroupNormalization(groups=64)(outputs)
    #outputs = Dropout(0.1)(outputs)
    outputs = MaxPooling1D(pool_size=1,strides=1)(outputs) if use1d else MaxPooling2D(pool_size=(1,1),strides=1)(outputs)
    outputs = Flatten()(outputs)
    outputs = Dense(dim)(outputs)
    outputs = Dropout(0.001)(outputs)
    outputs = Activation(PReLU())(outputs)
    model = Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer=AdamW(learning_rate=0.0001), loss='log_cosh')
    checkpoint_filepath = str(uuid.uuid1()).replace('-', '') + '.weights.h5'
    model_checkpoint_callback = keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_filepath,
        save_weights_only=True,
        monitor='val_loss',
        mode='min',
        save_best_only=True)
    model.fit(trainX, trainY, 
        validation_data=(testX, testY),
        batch_size=1,
        callbacks=[model_checkpoint_callback],
        epochs=100,
        verbose=1)
    model.load_weights(checkpoint_filepath)
    predY = model.predict(predX, batch_size=1)
    return predY

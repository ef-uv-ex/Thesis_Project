# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 12:51:50 2022

- I am using this code to practice building CNNs using the Keras functional API
- Goals:
    - Understand how the functional API coding style works
    - Understand the basic layers
    - Understand how to shape and input data to the model
    - Understand how to build the architecture of the model
    - Understand how to compile the model
    - Understand how to read the outputs of the model
    - Understand the results
    - Understand how to tune the model

@author: Administrator
"""
import tensorflow as tf
from tensorflow import keras
import numpy as np
import pickle as pkl



# y_train = keras.utils.to_categorical(y_train)
# y_test = keras.utils.to_categorical(y_test)
# Import training data
target_file = r'G:\Rofrano_Thesis\Project\data\Sim_Data_13Oct22.obj'
file = open(target_file, 'rb')
sim_data = pkl.load(file)
file.close()

# Import test data
target_file = r'G:\Rofrano_Thesis\Project\data\Meas_Data_13Oct22.obj'
file = open(target_file, 'rb')
meas_data = pkl.load(file)
file.close()

# Shuffle data
np.random.shuffle(sim_data)
X = sim_data[:, :-1, :]
y = sim_data[:, -1, 0].astype('uint32')

np.random.shuffle(meas_data)
Xt = meas_data[:, :-1, :]
yt = meas_data[:, -1, 0].astype('uint32')


# Train/Test split
num_classes = len(np.unique(y))
x_train = X  # [:60000]; can use the full set
y_train = keras.utils.to_categorical(y)

x_test = Xt  # X[60000:]; can use the full set
y_test = keras.utils.to_categorical(yt)

x_max = np.max(X)

""" Convolutional Neural Net Model is called functionally"""


def make_model(input_shape):
    input_layer = keras.layers.Input(input_shape)  # Define input tenosr shape

    """  First conv layer """
    conv1 = keras.layers.Conv1D(filters=64,  # 64 Filters per channel
                                kernel_size=3,  # Convolution of 3 segments
                                activation='relu',  # Relu activation
                                padding='same',  # Place zeros evenly on the left and right
                                )(input_layer)

    conv1 = keras.layers.MaxPooling1D(pool_size=2,  # Grab two adjacent conv products and pull max
                                      strides=2  # Move in strides of 2 to a new pair, halving the original input
                                      )(conv1)

    """ Second conv layer"""
    conv2 = keras.layers.Conv1D(filters=128,  # Increase network size for more features
                                kernel_size=3,  # Convolution of 3 segments
                                activation='relu',  # Relu activation
                                padding='same',  # Place zeros evenly on the left and right
                                )(conv1)

    conv2 = keras.layers.MaxPooling1D(pool_size=2,  # Grab two adjacent conv products and pull max
                                      strides=2  # Move in strides of 2 to a new pair, halving the original input
                                      )(conv2)

    """ Third Conv layer"""
    conv3 = keras.layers.Conv1D(filters=256,  # Increase network size for more features
                                kernel_size=3,  # Convolution of 3 segments
                                activation='relu',  # Relu activation
                                padding='same',  # Place zeros evenly on the left and right
                                )(conv2)

    conv3 = keras.layers.MaxPooling1D(pool_size=2,  # Grab two adjacent conv products and pull max
                                      strides=2  # Move in strides of 2 to a new pair, halving the original input
                                      )(conv3)

    """ Output """
    output = keras.layers.Flatten()(conv3)
    output = keras.layers.Dense(1024, activation="relu")(output)
    output = keras.layers.Dense(512, activation="relu")(output)
    output = keras.layers.Dense(256, activation="relu")(output)
    output_layer = keras.layers.Dense(num_classes, activation='softmax')(output)

    return keras.models.Model(inputs=input_layer, outputs=output_layer)


model = make_model(input_shape=x_train.shape[1:])  # Calls the shape excluding the sample size
model.summary()
keras.utils.plot_model(model, "Simple_NN_model.png", show_shapes=True)

# %% Compile the model
model.compile(
    optimizer="adam",  # Stochastic Gradient Descent using Adam
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# %% Fit model with training data
my_callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=2)  # Wait for a reduction in improvment over 2 epochs
]

history = model.fit(x_train, y_train,
                    batch_size=32,
                    epochs=100,
                    callbacks=my_callbacks,
                    validation_split=0.2  # pull 20% of the data for validation
                    )

# %% Test the model on the test data
test_scores = model.evaluate(x_test, y_test, verbose=2)
print("Test loss:", test_scores[0])
print("Test accuracy:", test_scores[1])

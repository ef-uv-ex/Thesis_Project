# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 12:51:50 2022

Current Model:

VGG19 -- Deep convolutional Neural Network
- Changing to VGG 19 model Neural netork
- Will be using the nose-1 data only
- Likely to switch to single fuselage categories

@author: Administrator
"""
import tensorflow as tf
from tensorflow import keras
import numpy as np
import pickle as pkl


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
y_train = y  #keras.utils.to_categorical(y)

x_test = Xt  # X[60000:]; can use the full set
y_test = yt  #keras.utils.to_categorical(yt)

x_max = np.max(X)

""" Convolutional Neural Net Model is called functionally"""
# Set the optimizers paramters


# Hyperparameter settings
LR = 0.001  # Learning rate
M = 0.9  # Momentum
DR = 0.5  # Dropout rate
BS = 300  # Batch Size
E = 100  # Epochs
#OPTIMIZER = SGD

adam = tf.keras.optimizers.Adam(
    learning_rate=LR,  # Default = 0.001
    beta_1=0.9,  # Default = 0.9
    beta_2=0.999,  # Default = 0.999
    epsilon=1e-07,  #
    amsgrad=False,
    name='Adam'
)

SGD = tf.keras.optimizers.SGD(
    learning_rate=LR,  # Default = 0.01
    momentum=M,  # Default = 0.0
    nesterov=False,  # Default = False
    name='SGD'
)
OPTIMIZER = SGD

def make_model(input_shape):
    input_layer = keras.layers.Input(input_shape)  # Define input tenosr shape

    """  First conv layer """
    conv1 = keras.layers.Conv1D(filters=64,
                                kernel_size=3,
                                activation='relu',
                                padding='same',
                                )(input_layer)

    conv1 = keras.layers.Conv1D(filters=64,
                                kernel_size=3,
                                activation='relu',
                                padding='same',
                                )(conv1)

    conv1 = keras.layers.MaxPooling1D(pool_size=2,
                                      strides=2
                                      )(conv1)

    """ Second conv layer"""
    conv2 = keras.layers.Conv1D(filters=128,
                                kernel_size=3,
                                activation='relu',
                                padding='same',
                                )(conv1)
    conv2 = keras.layers.Conv1D(filters=128,
                                kernel_size=3,
                                activation='relu',
                                padding='same',
                                )(conv2)

    conv2 = keras.layers.MaxPooling1D(pool_size=2,
                                      strides=2
                                      )(conv2)

    """ Third Conv layer"""
    conv3 = keras.layers.Conv1D(filters=256,
                                kernel_size=3,
                                activation='relu',
                                padding='same',
                                )(conv2)
    conv3 = keras.layers.Conv1D(filters=256,
                                kernel_size=3,
                                activation='relu',
                                padding='same',
                                )(conv3)
    conv3 = keras.layers.Conv1D(filters=256,
                                kernel_size=3,
                                activation='relu',
                                padding='same',
                                )(conv3)
    conv3 = keras.layers.Conv1D(filters=256,
                                kernel_size=3,
                                activation='relu',
                                padding='same',
                                )(conv3)
    conv3 = keras.layers.MaxPooling1D(pool_size=2,
                                      strides=2
                                      )(conv3)

    """ Fourth Conv layer"""
    conv4 = keras.layers.Conv1D(filters=512,
                                kernel_size=3,
                                activation='relu',
                                padding='same',
                                )(conv3)
    conv4 = keras.layers.Conv1D(filters=512,
                                kernel_size=3,
                                activation='relu',
                                padding='same',
                                )(conv4)
    conv4 = keras.layers.Conv1D(filters=512,
                                kernel_size=3,
                                activation='relu',
                                padding='same',
                                )(conv4)
    conv4 = keras.layers.Conv1D(filters=512,
                                kernel_size=3,
                                activation='relu',
                                padding='same',
                                )(conv4)
    conv4 = keras.layers.MaxPooling1D(pool_size=2,
                                      strides=2
                                      )(conv4)
    """ Fifth Conv layer"""
    conv5 = keras.layers.Conv1D(filters=512,
                                kernel_size=3,
                                activation='relu',
                                padding='same',
                                )(conv4)
    conv5 = keras.layers.Conv1D(filters=512,
                                kernel_size=3,
                                activation='relu',
                                padding='same',
                                )(conv5)
    conv5 = keras.layers.Conv1D(filters=512,
                                kernel_size=3,
                                activation='relu',
                                padding='same',
                                )(conv5)
    conv5 = keras.layers.Conv1D(filters=512,
                                kernel_size=3,
                                activation='relu',
                                padding='same',
                                )(conv5)
    conv5 = keras.layers.MaxPooling1D(pool_size=2,
                                      strides=2
                                      )(conv5)

    """ Output """
    output = keras.layers.Flatten()(conv5)
    output = keras.layers.Dense(4096,
                                activity_regularizer=keras.regularizers.L2(5e-4),
                                activation="relu")(output)
    output = keras.layers.Dropout(DR)(output)
    output = keras.layers.Dense(4095,
                                activity_regularizer=keras.regularizers.L2(5e-4),
                                activation="relu")(output)
    output = keras.layers.Dropout(DR)(output)
    output = keras.layers.Dense(1000,
                                activity_regularizer=keras.regularizers.L2(5e-4),
                                activation="relu")(output)
    output_layer = keras.layers.Dense(num_classes, activation='softmax')(output)

    return keras.models.Model(inputs=input_layer, outputs=output_layer)


model = make_model(input_shape=x_train.shape[1:])  # Calls the shape excluding the sample size
model.summary()
keras.utils.plot_model(model, "VGG_19.png", show_shapes=True)


# %% Compile the model
model.compile(
    optimizer=OPTIMIZER,  # Stochastic Gradient Descent using Adam
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# %% Fit model with training data
my_callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=2)  # Wait for a reduction in improvment over 2 epochs
]

history = model.fit(x_train, y_train,
                    batch_size=BS,
                    epochs=E,
                    callbacks=my_callbacks,
                    validation_split=0.2  # pull 20% of the data for validation
                    )

# %% Test the model on the test data
test_scores = model.evaluate(x_test, y_test, verbose=2)
print("Test loss:", test_scores[0])
print("Test accuracy:", test_scores[1])

y_pred = model.predict(x_test)

matrix = tf.math.confusion_matrix(y_test, np.argmax(y_pred, axis=1))

import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use('rad_style')  # Save in the 'stylelib' folder in '.matplotlib' of C: directory

ax = plt.axes()
label_count=len(np.unique(y_test))
categories=['nose-1', 'body_left', 'tail', 'body_right']
cfm = sns.heatmap(matrix/np.sum(matrix), annot=True, fmt='.2%', cmap='Blues',
            xticklabels=categories,
            yticklabels=categories,
            ax = ax)

ax.set_title("Confusion Matrix \n labels="+str(label_count)
          +", Batch Size="+str(BS)+',\n Learning Rate='+str(LR)
          +", Momentum="+str(M))



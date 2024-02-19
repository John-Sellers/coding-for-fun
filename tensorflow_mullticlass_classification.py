import tensorflow as tf
from tensorflow.keras.datasets import fashion_mnist
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

# The data has already be divided into training and testing. We just
# need to store them in variables
(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
print(
    f"{X_train.shape = }\n",
    f"{y_train.shape = }\n",
    f"{X_test.shape = }\n",
    f"{y_test.shape = }\n",
)
X_train[0], y_train[0]
plt.imshow(X_train[15])
y_train[15]
# Create list of outputs so we know what is what
class_names = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle Boot",
]
len(class_names)
index = 2200
plt.imshow(X_train[index], cmap=plt.cm.binary)
plt.title(class_names[y_train[index]])
import random

plt.figure(figsize=(5, 5))
for i in range(4):
    ax = plt.subplot(2, 2, i + 1)
    rand_index = random.choice(range(len(X_train)))
    plt.imshow(X_train[rand_index], cmap=plt.cm.binary)
    plt.title(class_names[y_train[rand_index]])
    plt.axis(False)
flatten_model = tf.keras.Sequential()
flatten_model.add(tf.keras.layers.InputLayer(input_shape=(28, 28)))
flatten_model.add(tf.keras.layers.Flatten())
flatten_model.output_shape
y_train[:10]
y_train.shape, X_train.shape
# Assuming y_train is not one-hot encoded
# One-hot encode the labels
y_train_encoded = tf.keras.utils.to_categorical(y_train, num_classes=10)

# Rest of your code remains unchanged
tf.random.set_seed(0)

model = tf.keras.Sequential()
model.add(tf.keras.layers.InputLayer(input_shape=(28, 28)))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(4, activation="relu"))
model.add(tf.keras.layers.Dense(4, activation="relu"))
model.add(tf.keras.layers.Dense(10, activation="softmax"))

lr = 0.001
optimizer = tf.keras.optimizers.Adam(learning_rate=lr)
model.compile(
    loss=tf.keras.losses.CategoricalCrossentropy(),
    optimizer=optimizer,
    metrics=["accuracy"],
)

es = tf.keras.callbacks.EarlyStopping(monitor="loss")

history = model.fit(
    X_train,
    y_train_encoded,
    epochs=10,
    callbacks=[es],
    validation_data=(X_test, tf.one_hot(y_test, depth=10)),
)
model.summary()
X_train.min(), X_train.max()
# Normalizing data
X_train_norm = X_train / 255.0
X_test_norm = X_test / 255.0

# Checking min and max value of normalized data
X_train_norm.min(), X_train_norm.max()
model2 = tf.keras.Sequential()
model2.add(tf.keras.layers.InputLayer(input_shape=(28, 28)))
model2.add(tf.keras.layers.Flatten())
model2.add(tf.keras.layers.Dense(4, activation="relu"))
model2.add(tf.keras.layers.Dense(4, activation="relu"))
model2.add(tf.keras.layers.Dense(10, activation="softmax"))

lr = 0.01
optimizer = tf.keras.optimizers.Adam(learning_rate=lr)

model2.compile(
    loss=tf.keras.losses.CategoricalCrossentropy(),
    optimizer=optimizer,
    metrics=["accuracy"],
)

es = tf.keras.callbacks.EarlyStopping(monitor="loss")

history = model2.fit(
    X_train_norm,
    y_train_encoded,
    epochs=10,
    validation_data=(X_test_norm, tf.one_hot(y_test, depth=10)),
)

print('Importing...')
import dataset_creator

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers, losses
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import Model

def create_dataset(num_imgs):
  print('Loading dataset...')

  train_data, noisy_train_data = dataset_creator.load_data(80) #8000
  test_data, noisy_test_data = dataset_creator.load_data(10) #1000

  x_train = train_data.astype('float32') / 255.
  x_train_noisy = noisy_train_data.astype('float32') / 255.
  x_test = test_data.astype('float32') / 255.
  x_test_noisy = noisy_test_data.astype('float32') / 255.

  x_train = x_train[..., tf.newaxis]
  x_train_noisy = x_train_noisy[..., tf.newaxis]
  x_test = x_test[..., tf.newaxis]
  x_test_noisy = x_test_noisy[..., tf.newaxis]

  # n = 10
  # plt.figure(figsize=(20, 2))
  # for i in range(n):
  #     ax = plt.subplot(1, n, i + 1)
  #     plt.title("original + noise")
  #     plt.imshow(tf.squeeze(x_test_noisy[i]))
  #     plt.gray()
  # plt.show()
  return x_train, x_train_noisy, x_test, x_test_noisy


class Denoise(Model):
  def __init__(self, model_path):
    super(Denoise, self).__init__()
    self.encoder = tf.keras.Sequential([
      layers.Input(shape=(256, 256, 1)), 
      layers.Conv2D(16, (3,3), activation='relu', padding='same', strides=2),
      layers.Conv2D(32, (3,3), activation='relu', padding='same', strides=2)])

    self.decoder = tf.keras.Sequential([
      layers.Conv2DTranspose(32, kernel_size=3, strides=2, activation='relu', padding='same'),
      layers.Conv2DTranspose(16, kernel_size=3, strides=2, activation='relu', padding='same'),
      layers.Conv2D(1, kernel_size=(3,3), activation='sigmoid', padding='same')])
    if(model_path):
      try:
          self = keras.models.load_model(MODEL_PATH)
      except:
          self.compile(optimizer='adam', loss=losses.MeanSquaredError())

  def call(self, x):
    encoded = self.encoder(x)
    decoded = self.decoder(encoded)
    return decoded

  # def train(self, x_train, y_train, x_test, y_test):
  #   self.fit(y_train, x_train, 
  #               epochs=5,
  #               shuffle=True,
  #               validation_data=(y_test, x_test))

  #   autoencoder.encoder.summary()

  # def test(self, x_test, y_test):
  #   decoded_imgs = autoencoder.call(imgs)
  #   n = 10
  #   plt.figure(figsize=(20, 4))
  #   for i in range(n):
  #     # display original + noise
  #     ax = plt.subplot(2, n, i + 1)
  #     plt.title("original + noise")
  #     plt.imshow(tf.squeeze(x_test_noisy[i]))
  #     plt.gray()
  #     ax.get_xaxis().set_visible(False)
  #     ax.get_yaxis().set_visible(False)

  #     # display reconstruction
  #     bx = plt.subplot(2, n, i + n + 1)
  #     plt.title("reconstructed")
  #     plt.imshow(tf.squeeze(decoded_imgs[i]))
  #     plt.gray()
  #     bx.get_xaxis().set_visible(False)
  #     bx.get_yaxis().set_visible(False)
  #   plt.show()

autoencoder = Denoise()

autoencoder.compile(optimizer='adam', loss=losses.MeanSquaredError())
autoencoder = keras.models.load_model('../models/test')

autoencoder.fit(x_train_noisy, x_train,
                epochs=5,
                shuffle=True,
                validation_data=(x_test_noisy, x_test))

autoencoder.save('../models/test')


autoencoder.encoder.summary()

# encoded_imgs = autoencoder.encoder(x_test).numpy()
# decoded_imgs = autoencoder.decoder(encoded_imgs).numpy()

decoded_imgs = autoencoder.call(x_test)

n = 10
plt.figure(figsize=(20, 4))
for i in range(n):

    # display original + noise
    ax = plt.subplot(2, n, i + 1)
    plt.title("original + noise")
    plt.imshow(tf.squeeze(x_test_noisy[i]))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # display reconstruction
    bx = plt.subplot(2, n, i + n + 1)
    plt.title("reconstructed")
    plt.imshow(tf.squeeze(decoded_imgs[i]))
    plt.gray()
    bx.get_xaxis().set_visible(False)
    bx.get_yaxis().set_visible(False)
plt.show()




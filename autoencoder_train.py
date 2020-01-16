from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import keras
from keras.layers import Activation, Dense, Input
from keras.layers import Conv2D, Flatten
from keras.layers import Reshape, Conv2DTranspose
from keras.models import Model
from keras import backend as K
from keras.datasets import mnist
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance
import matplotlib.image as mpimg

np.random.seed(1337)


def get_image(fileName):
  im = Image.open(fileName)
  image = Image.fromarray(im / np.amax(im) * 255)
  # im.mode = 'I'
  im = im.point(lambda i:i*(1./256)).convert('L')
  size = 32, 32
  image.thumbnail(size, Image.ANTIALIAS)
  # enhancer = ImageEnhance.Brightness(im)
  # enhanced_im = enhancer.enhance(2.0)
  # im.save("enhanced.sample1.png")
  # exit()
  # return enhanced_im
  return image

def load_train_img(fileName):
  image = Image.open(fileName)
  # image = Image.fromarray(im / np.amax(im) * 255)
  arr = np.asarray(image)
  split = arr.shape[1]/32 #256
  arr = np.split(arr, split)
  arr = np.array([np.split(x, split, 1) for x in arr])
  return arr

# MNIST dataset
# (x_train, _), (x_test, _) = mnist.load_data()
# print('MNIST Shape: ', x_train.shape)

# Microscope dataset
# train = []
# for i in range(1,120):
#   fileName = 'canal_1/s_C001T'
#   fileName += '%0*d' % (3, i)
#   fileName += '.tif'
#   # train.append(mpimg.imread(fileName))
#   # exit()
#   im = get_image(fileName)
#   train.append(np.array(im))
# x_train = np.asarray(train)
# print('TPP Shape: ', x_train.shape)

# Microscope dataset
train = []
for i in range(1,16):
  arr = load_train_img('train/train%d.tif' % i)
  for row in arr:
    for im in row:
      # print(im.shape)
      train.append(im)
x_train = np.asarray(train)


test = [ x_train[1], x_train[2], ]
for i in range(1,20): #151):
  fileName = 'canal_1/s_C001T'
  fileName += '%0*d' % (3, i)
  fileName += '.tif'
  im = get_image(fileName)
  test.append(np.array(im))
x_test = np.asarray(test)


# img=mpimg.imread('croped_image.tif')
# print([img])

image_size = x_train.shape[1]
x_train = np.reshape(x_train, [-1, image_size, image_size, 1])
x_test = np.reshape(x_test, [-1, image_size, image_size, 1])
x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

# Generate corrupted MNIST images by adding noise with normal dist
# centered at 0.5 and std=0.5
noise = np.random.normal(loc=0.5, scale=0.5, size=x_train.shape)
x_train_noisy = x_train + noise
# noise = np.random.normal(loc=0.5, scale=0.5, size=x_test.shape)
x_test_noisy = x_test

x_train_noisy = np.clip(x_train_noisy, 0., 1.)
x_test_noisy = np.clip(x_test_noisy, 0., 1.)

# Network parameters
input_shape = (image_size, image_size, 1)
batch_size = 128
kernel_size = 3
# Vamos a tener que agrandar esto seguro
latent_dim = 16
# Encoder/Decoder number of CNN layers and filters per layer
layer_filters = [32, 64]

# Build the Autoencoder Model
# First build the Encoder Model
inputs = Input(shape=input_shape, name='encoder_input')
x = inputs
# Stack of Conv2D blocks
# Notes:
# 1) Use Batch Normalization before ReLU on deep networks
# 2) Use MaxPooling2D as alternative to strides>1
# - faster but not as good as strides>1
for filters in layer_filters:
    x = Conv2D(filters=filters,
               kernel_size=kernel_size,
               strides=2,
               activation='relu',
               padding='same')(x)

# Shape info needed to build Decoder Model
shape = K.int_shape(x)

# Generate the latent vector
x = Flatten()(x)
latent = Dense(latent_dim, name='latent_vector')(x)

# Instantiate Encoder Model
encoder = Model(inputs, latent, name='encoder')
encoder.summary()

# Build the Decoder Model
latent_inputs = Input(shape=(latent_dim,), name='decoder_input')
x = Dense(shape[1] * shape[2] * shape[3])(latent_inputs)
x = Reshape((shape[1], shape[2], shape[3]))(x)

# Stack of Transposed Conv2D blocks
# Notes:
# 1) Use Batch Normalization before ReLU on deep networks
# 2) Use UpSampling2D as alternative to strides>1
# - faster but not as good as strides>1
for filters in layer_filters[::-1]:
    x = Conv2DTranspose(filters=filters,
                        kernel_size=kernel_size,
                        strides=2,
                        activation='relu',
                        padding='same')(x)

x = Conv2DTranspose(filters=1,
                    kernel_size=kernel_size,
                    padding='same')(x)

outputs = Activation('sigmoid', name='decoder_output')(x)

# Instantiate Decoder Model
decoder = Model(latent_inputs, outputs, name='decoder')
decoder.summary()

# Autoencoder = Encoder + Decoder
# Instantiate Autoencoder Model
autoencoder = Model(inputs, decoder(encoder(inputs)), name='autoencoder')
autoencoder.summary()

autoencoder.compile(loss='mse', optimizer='adam')

# Train the autoencoder
autoencoder.fit(x_train_noisy,
                x_train,
                validation_data=(x_test_noisy, x_test),
                epochs=5,
                batch_size=batch_size)
# Save the autoencoder´s weights
autoencoder.save('models/autoencoder_model.h5')

# Predict the Autoencoder output from corrupted test images
x_decoded = autoencoder.predict(x_test_noisy)

# Display the 1st 8 corrupted and denoised images
rows, cols = 4, 4
num = rows * cols
imgs = np.concatenate([x_test[:num], x_test_noisy[:num], x_decoded[:num]])
imgs = imgs.reshape((rows * 3, cols, image_size, image_size))
imgs = np.vstack(np.split(imgs, rows, axis=1))
imgs = imgs.reshape((rows * 3, -1, image_size, image_size))
imgs = np.vstack([np.hstack(i) for i in imgs])
imgs = (imgs * 255).astype(np.uint8)
plt.figure()
plt.axis('off')
plt.title('Original images: top rows, '
          'Corrupted Input: middle rows, '
          'Denoised Input:  third rows')
plt.imshow(imgs, interpolation='none', cmap='gray')
Image.fromarray(imgs).save('corrupted_and_denoised.png')
plt.show()
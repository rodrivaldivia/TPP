import argparse
MODEL_PATH = '../models/test'
DATASET_SIZE = 20

parser = argparse.ArgumentParser(description='Run the image denoiser model')

parser.add_argument('--train', help='Train the model', action='store_true')

args = parser.parse_args()

from dataset_autoencoder import Denoise, create_dataset
from tensorflow import keras

# try:
#     autoencoder = keras.models.load_model(MODEL_PATH)
# except:
#     autoencoder = Denoise()
#     newModel = True

if(args.train):
	# FIT
	x_train, y_train, x_test, y_test = create_dataset(DATASET_SIZE)
	autoencoder.train(x_train, y_train, x_test, y_test)
	autoencoder.save(MODEL_PATH)

	autoencoder.test(x_test, y_test)

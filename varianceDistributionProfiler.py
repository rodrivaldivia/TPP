import numpy as np
from PIL import Image, ImageEnhance
import functools as tools
import ctypes
from os import listdir
import matplotlib.pyplot as plt
from os.path import isfile, join




def load_image_array(fileName):
	image = Image.open(fileName)
	arr = np.asarray(image).astype(np.int16)
	return arr

def get_images_delta(first_array, second_array):
	return np.subtract(first_array, second_array)


def calculate_noise_distribution(array_collection):
	concat = np.concatenate(array_collection).ravel().tolist()
	return concat

def value_cmp(a, b):
    if a[1] > b[1]:
        return -1
    elif a[1] == b[1]:
        if a[0] > b[0]:
            return 1
        else:
            return -1
    else:
        return 1

def add_ocurrency_to_dictionary(element, dictionary):
	if(element in dictionary):
		dictionary[element] += 1
	else:
		dictionary[element]= 1
	return element

def dictionary_to_arrays(ocurrencies_dict):
	keys = ocurrencies_dict.keys()
	elements = []
	for key in keys:
		elements.append((key, ocurrencies_dict[key]))
	sorted_elements = sorted(elements, key=lambda x: x[0])
	keys = []
	values = []
	for element in sorted_elements:
		keys.append(element[0])
		values.append(element[1])
	return keys, values


def get_plotable_arrays(ocurrencies_list):
	ocurrencies_dictionary = {}
	fillDictionary = lambda x: add_ocurrency_to_dictionary(x,ocurrencies_dictionary)
	mappingFunction = np.vectorize(fillDictionary)
	mappingFunction(ocurrencies_list)
	return dictionary_to_arrays(ocurrencies_dictionary)




def main(mypath):
	files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	last_file = None
	deltas_list = []
	for file in files:
		if(not last_file):
			last_file=file
			continue
		last_image = load_image_array(mypath+'/'+file)
		current_image = load_image_array(mypath+'/'+last_file)
		deltas = get_images_delta(last_image, current_image)
		deltas_list.append(deltas)
		last_file=file
	ocurrencies = calculate_noise_distribution(deltas_list[:])
	print(len(deltas_list), "Fotos se procesaron")
	keys, values = get_plotable_arrays(ocurrencies)
	correctable_pixels = tools.reduce(lambda x,y: x+y, keys[7:])
	print(correctable_pixels)
	hist, bins = np.histogram(values, keys)
	plt.hist(hist, bins)
	plt.yscale('log')
	plt.show()



main('./canal_1')



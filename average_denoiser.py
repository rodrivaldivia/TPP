import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance

def load_train_img(fileName):
  im = Image.open(fileName)
  im = im.point(lambda i:i*(1./256)).convert('L')
  return im

def load_img(num):
	fileName = 'canal_1/s_C001T'
	fileName += '%0*d' % (3, num)
	fileName += '.tif'
	return load_train_img(fileName)

def save_img(img, num):
	fileName = 'train/s_C001T'
	fileName += '%0*d' % (3, num)
	fileName += '.tif'
	img.save(fileName)

# for i in range(2,130):
for i in range(2,3):
	before = load_img(i-1)
	current = load_img(i)
	after = load_img(i+1)

	blendIm = Image.blend(after, before, 0.5)
	current = ImageEnhance.Contrast(current).enhance(1.2)
	final = Image.blend(current, blendIm, 0.75)
	save_img(final, i)


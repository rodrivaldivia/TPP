from PIL import Image, ImageDraw
from scipy import asarray as ar, exp, sqrt
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

def showImage(im, points):
	drawable_image = ImageDraw.Draw(im)
	drawable_image.line(points, fill='#00ffff', width = 5, joint='curve')
	im.show()

def correctPoints(im, points):
	arr = np.array(im.point(lambda i:i*(1./256)).convert('L'))
	# print(a[:3])
	# point = points[2]
	newPoints = []
	for point in points:
		# brightness_profiler(arr[point[1], point[0]-20:point[0]+20])
		newPoint = getNewMean(arr, point)
		# print(point)
		# print(newPoint)
		newPoints.append(newPoint)
	return newPoints

def getNewMean(imageArray, point):
	newPoint = point
	minX = max(point[0]-10, 0)
	maxX = min(point[0]+10, 255)
	array = imageArray[point[1], minX:maxX]
	x = fitFunction(array).item(1)
	# x = fitFunction(array)
	newPoint = (x + minX, point[1])
	return newPoint


# Interpolation inital value
vi = 0

def interpolation(value, beta):
	global vi
	vi = beta * vi + (1 - beta) *value
	return vi

def gaus(x,a,mu,sigma):
    return a*exp(-(x-mu)**2/(2*sigma**2))

def fitFunction(data):
	points = range(len(data))
	# n = len(data)
	# # print(n)
	# mean = sum(data*points)/n
	# return mean
	popt,pcov = curve_fit(gaus, points, data, maxfev = 10000)
	return popt

def brightness_profiler(array):
	points = [ i for i in range(len(array))]
	values = [ interpolation(i, 0.5) for i in array ]
	xx = np.linspace( 0, 50, 100 )  ## <--- calculate against a continuous variable
	popt = fitFunction(array)
	plt.plot(points, values, label='brightness')
	plt.plot(xx,gaus(xx,*popt),'r',label='fit') 
	plt.xlabel('pixeles')
	plt.ylabel('brightness')

	plt.title("Brightness Profiler")

	plt.legend()

	plt.show()
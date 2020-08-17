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
	for index, point in enumerate(points):
		# brightness_profiler(arr[point[1], point[0]-20:point[0]+20])
		vector = tuple([1,1])
		if(index > 0):
			vector = tuple(map(lambda x, y: x - y, point, points[index - 1]))
		else:
			vector = tuple(map(lambda x, y: x - y, points[index + 1], point))

		slope = 0
		if(vector[1] != 0):
			slope = -vector[0]/vector[1]
		# print(vector, slope)
		newPoint = getNewMean(arr, point, slope)
		# print(point)
		# print(newPoint)
		newPoints.append(newPoint)
	return newPoints

def boundIndexes(number):
	newNum = max(number, 0)
	newNum = min(255, newNum)
	return newNum

def getNewMean(imageArray, point, slope):
	newPoint = point
	minX = max(point[0]-25, 0)
	maxX = min(point[0]+25, 255)
	#  Esta linea se cambia por la version con pendiente
	points = []
	for i in range(-25, 25):
		x = round(point[0] + i)
		y = round(point[1] + i*slope)
		x = boundIndexes(x);
		y = boundIndexes(y);
		points.append((x,y));
		# print(i, x, y, imageArray[(x, y)]);

	# oldArray = imageArray[point[1], minX:maxX]
	# print(oldArray)
	array = np.array([imageArray[(e[1],e[0])] for e in points])
	# print(array)
	# x = fitFunction(array).item(1)
	x = fitManually(array)
	# print(x)
	newPoint = (x + minX, point[1]) # y = oldY + x*slope
	return newPoint


def fitManually(array):
	arraySum = 0
	for i, point in enumerate(array):
		arraySum += i*point
	return arraySum/sum(array)


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
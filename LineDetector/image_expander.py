from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy import asarray as ar, exp, sqrt
from scipy.optimize import curve_fit
import pygame








# Como queremos poder rotar las imagenes sin que estas pierdan informacion lo que hacemos
# es ponerlas dentro de un marco mas grande de forma que todos los pixeles puedan rotar dentro de
# ese marco sin perder pixeles, agregando 110 pixeles en total vertical y horizontalmente aseguramos
# que la imagen pueda rotar libremente
#Nuevas imagen de 366 x 366

def expand_image(url):
	image = Image.open(url)
	arrayed_image = np.array(image)
	blank_container = np.zeros((366,366)) + 255
	blank_container[55: 311, 55:311] = arrayed_image
	return Image.fromarray(blank_container)

# Valor inicial de interpolacion
vi = 0

def interpolation(value, beta):
	global vi
	vi = beta * vi + (1 - beta) *value
	return vi

def gaus(x,a,mu,sigma):
    return a*exp(-(x-mu1)**2/(2*sigma1**2))

def fitFunction(data):
	points = [ i for i in range(len(data)) ]
	n = len(data) 
	mean = sum(data*points)/n
	sigma = sqrt(sum(data*(points-mean)**2)/n)
	popt,pcov = curve_fit(gaus, points, data, maxfev=15000)  ## <--- leave out the first estimation of the parameters
	return popt

def brightness_profiler(array):
	points = [ i for i in range(len(array))]
	values = [ interpolation(i, 0.2) for i in array ]
	print(points)
	xx = np.linspace( 0, 50, 100 )  ## <--- calculate against a continuous variable
	popt = fitFunction(array)
	plt.plot(points, values, label='brightness')
	plt.plot(xx,gaus(xx,*popt),'r',label='fit') 
	plt.xlabel('pixeles')
	plt.ylabel('brightness')

	plt.title("Brightness Profiler")

	plt.legend()

	plt.show()




def checkMouseInImage(event):
	try:
		position = event.pos
		print("Probamos")
		return position[0] >= 0 and position[0] < 256 and position[1] >= 0 and position[1] < 256
	except:
		print("Fallo")
		return False

im = Image.open("./s_C001T006.tif")
a = np.array(im)
print(a[:3])
brightness_profiler(a[70, 70:120])
a[69, 70:120] = 255
a[70, 70:120] = 255
a[71, 70:120] = 255
b = Image.fromarray(a)
b.show()
# out = im.convert("RGB")
# out.save('pnged_first_image.png', "PNG", quality=100)


# pygame.init()

# window_width=400
# window_height=400

# animation_increment=10
# clock_tick_rate=20

# # Open a window
# size = (window_width, window_height)
# screen = pygame.display.set_mode(size)
# screen.fill([255,255,255])

# # Set title to the window
# pygame.display.set_caption("Visor de microtubulos")

# dead=False

# clock = pygame.time.Clock()
# background_image = pygame.image.load('./pnged_first_image.png').convert()

# clicked = False

# while(dead==False):
# 	for event in pygame.event.get():
# 		if event.type == pygame.MOUSEBUTTONDOWN:
# 			clicked = True
# 		if event.type == pygame.MOUSEBUTTONUP:
# 			clicked = False
# 		if clicked and checkMouseInImage(event):
# 			# print(event, event.pos)
# 			print("Pintamos")
# 			pygame.draw.circle(background_image, (0,255,0,0.1), event.pos, 7)
# 		if event.type == pygame.QUIT:
# 			dead = True

# 	screen.blit(background_image, [0, 0])

# 	pygame.display.flip()
# 	clock.tick(clock_tick_rate) 
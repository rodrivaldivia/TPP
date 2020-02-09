from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
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


def brightness_profiler(array):
	points = [ i for i in range(len(array))]
	print(points)
	plt.plot(points, array, label='brightness')
	plt.xlabel('pixes')
	plt.ylabel('brightness')

	plt.title("Brightness Profiler")

	plt.legend()

	plt.show()


# Valor inicial de interpolacion
vi = 0

def interpolation(value, beta):
	global vi
	vi = beta * vi + (1 - beta) *value
	return vi

def checkMouseInImage(event):
	try:
		position = event.pos
		print("Probamos")
		return position[0] >= 0 and position[0] < 256 and position[1] >= 0 and position[1] < 256
	except:
		print("Fallo")
		return False

im = Image.open("./Images/canal1/s_C001T001.tif")
out = im.convert("RGB")
out.save('pnged_first_image.png', "PNG", quality=100)


pygame.init()

window_width=400
window_height=400

animation_increment=10
clock_tick_rate=20

# Open a window
size = (window_width, window_height)
screen = pygame.display.set_mode(size)
screen.fill([255,255,255])

# Set title to the window
pygame.display.set_caption("Visor de microtubulos")

dead=False

clock = pygame.time.Clock()
background_image = pygame.image.load('./pnged_first_image.png').convert()

clicked = False

while(dead==False):
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = True
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		if clicked and checkMouseInImage(event):
			# print(event, event.pos)
			print("Pintamos")
			pygame.draw.circle(background_image, (0,255,0,0.1), event.pos, 7)
		if event.type == pygame.QUIT:
			dead = True

	screen.blit(background_image, [0, 0])

	pygame.display.flip()
	clock.tick(clock_tick_rate) 
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pygame

def checkMouseInImage(event):
	try:
		position = event.pos
		# print("Probamos")
		return position[0] >= 0 and position[0] < 256 and position[1] >= 0 and position[1] < 256
	except:
		# print("Fallo")
		return False

def create():

	pygame.init()

	window_width=256
	window_height=256

	animation_increment=10
	clock_tick_rate=20

	# Open a window
	size = (window_width, window_height)
	screen = pygame.display.set_mode(size)
	screen.fill([255,255,255])

	# Set title to the window
	pygame.display.set_caption("Elegí los puntos del filamento")

	dead=False
	coordenates = []

	clock = pygame.time.Clock()

	im = Image.open('Images/canal_1/s_C001T001.tif')
	im = im.point(lambda i:i*(1./256)).convert('L')
	im.save('Images/canal_1/s_C001T001.png')
	background_image = pygame.image.load('Images/canal_1/s_C001T001.png').convert()



	clicked = False

	while(dead==False and len(coordenates)<10):
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				clicked = True
			if event.type == pygame.MOUSEBUTTONUP:
				clicked = False
			if clicked and checkMouseInImage(event):
				# print("Pintamos")
				# print(coordenates)
				coordenates.append(event.pos)
				pygame.draw.circle(background_image, (0,255,0,0.1), event.pos, 7)
			if event.type == pygame.QUIT:
				dead = True

		screen.blit(background_image, [0, 0])

		pygame.display.flip()
		clock.tick(clock_tick_rate)
	return coordenates
import math 
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImagePath

IMG_SIZE = 28 # 256

def generate_noise_img():
	# noise_img = Image.new("L", (IMG_SIZE,IMG_SIZE),'#000').convert('RGBA')
	# imarray = np.random.rand(IMG_SIZE,IMG_SIZE,3) * 50
	
	# Best aprox w/out noise profile
	mean = 10
	var = 60
	sigma = var ** 0.5
	gaussian = np.random.normal(mean, sigma, (IMG_SIZE,IMG_SIZE,3))
	# Make it darker
	gaussian = gaussian + 20

	noise_img = Image.fromarray(gaussian.astype('uint8')).convert("RGBA")
	# noise_img.show()
	return noise_img

def draw_straight_line_top(drawable_image):
	line_length = 400
	x1 , y1 = random.randint(0,IMG_SIZE), 0 
	angle = random.randint(0,180)
	angle_sin = np.sin(angle* np.pi / 180)
	angle_cos = np.cos(angle* np.pi / 180)
	adyacent_cathetus = angle_sin*line_length
	oposite_cathetus = angle_cos*line_length
	x2, y2 = 0, 0
	if(angle > 90):
		x2 = x1 + oposite_cathetus
		y2 = y1 + adyacent_cathetus
	else:
		x2 = x1 - oposite_cathetus
		y2 = y1 + adyacent_cathetus
	drawable_image.line([x1, y1, x2, y2], fill=(180,180,180,random.randint(100,255)), width = 4, joint='curve')

def draw_straight_line_left(drawable_image):
	line_length = 400
	x1 , y1 =  0, random.randint(0,IMG_SIZE)
	angle = random.randint(0,180)
	angle_sin = np.sin(angle* np.pi / 180)
	angle_cos = np.cos(angle* np.pi / 180)
	adyacent_cathetus = angle_sin*line_length
	oposite_cathetus = angle_cos*line_length
	x2, y2 = 0, 0
	if(angle > 90):
		x2 = x1 - oposite_cathetus
		y2 = y1 - adyacent_cathetus
	else:
		x2 = x1 + oposite_cathetus
		y2 = y1 + adyacent_cathetus
	drawable_image.line([x1, y1, x2, y2], fill=(180,180,180,random.randint(100,255)), width = random.randint(1,4), joint='curve')

def draw_curve_line_top(drawable_image):
	step_length = 10
	x1 , y1 = random.randint(0,IMG_SIZE), 0 
	line = [ x1, y1 ]
	initial_angle = random.randint(0,180)
	direction = random.randint(0,1)
	angle = initial_angle
	x2, y2 = 0, 0
	for i in range(30):
		angle_sin = np.sin(angle* np.pi / 180)
		angle_cos = np.cos(angle* np.pi / 180)
		adyacent_cathetus = angle_sin*step_length
		oposite_cathetus = angle_cos*step_length
		if(angle > 90):
			x2 = x1 + oposite_cathetus
			y2 = y1 + adyacent_cathetus
		else:
			x2 = x1 - oposite_cathetus
			y2 = y1 + adyacent_cathetus
		line.extend([x2,y2])
		x1 , y1 = x2, y2
		if(direction == 0):
			angle = angle + abs(random.randint(0,5))
		else:
			angle = angle - abs(random.randint(0,5))
	drawable_image.line(line, fill=(180,180,180,random.randint(100,255)), width = random.randint(1,4), joint='curve')


def draw_curve_line_left(drawable_image):
	step_length = 10
	x1 , y1 =  0, random.randint(0,IMG_SIZE)
	line = [ x1, y1 ]
	initial_angle = random.randint(0,180)
	direction = random.randint(0,1)
	angle = initial_angle
	x2, y2 = 0, 0
	for i in range(40):
		angle_sin = np.sin(angle* np.pi / 180)
		angle_cos = np.cos(angle* np.pi / 180)
		adyacent_cathetus = angle_sin*step_length
		oposite_cathetus = angle_cos*step_length
		if(angle > 90):
			x2 = x1 - oposite_cathetus
			y2 = y1 - adyacent_cathetus
		else:
			x2 = x1 + oposite_cathetus
			y2 = y1 + adyacent_cathetus
		line.extend([x2,y2])
		x1 , y1 = x2, y2
		# print(angle)
		if(direction == 0):
			angle = angle + abs(random.randint(0,5))
		else:
			angle = angle - abs(random.randint(0,5))
	drawable_image.line(line, fill=(180,180,180,random.randint(100,255)), width = random.randint(1,4), joint='curve')


# MAIN

def get_img_pair():
	clean_filaments = Image.new('RGBA', (IMG_SIZE,IMG_SIZE), (255,255,255,0))

	drawable_image = ImageDraw.Draw(clean_filaments)


	draw_straight_line_top(drawable_image)
	draw_straight_line_left(drawable_image)
	draw_curve_line_top(drawable_image)
	draw_curve_line_left(drawable_image)

	draw_straight_line_top(drawable_image)
	draw_straight_line_left(drawable_image)
	draw_curve_line_top(drawable_image)
	draw_curve_line_left(drawable_image)

	noise_img = generate_noise_img()

	blured_filaments = clean_filaments.filter(ImageFilter.GaussianBlur(radius=2))
	noisy_blured_filaments = Image.alpha_composite(noise_img, blured_filaments)

	# clean_out = blured_filaments.convert("LA")
	clean_out = blured_filaments.convert("L")
	noisy_out = noisy_blured_filaments.convert("L")

	# clean_out.show()
	# noisy_out.show()

	return clean_out, noisy_out

def load_data(size):
	train_data = []
	test_data = []
	for i in range(size):
		imgs = get_img_pair()
		train_data.append(np.array(imgs[0]))
		test_data.append(np.array(imgs[1]))
	return np.array(train_data), np.array(test_data)


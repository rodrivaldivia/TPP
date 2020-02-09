import math 
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImagePath

# new_image = Image.new("L", (256,256),'#000').convert('RGBA')
imarray = np.random.rand(256,256,3) * 50
new_image = Image.fromarray(imarray.astype('uint8')).convert('RGBA')

base = Image.new('RGBA', (256,256), (255,255,255,0))

drawable_image = ImageDraw.Draw(base)


def draw_straight_line_top(drawable_image):
	line_length = 400
	x1 , y1 = random.randint(0,256), 0 
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
	x1 , y1 =  0, random.randint(0,256)
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
	x1 , y1 = random.randint(0,256), 0 
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
			angle = angle +  abs(random.randint(0,5))
		else:
			angle = angle - abs(random.randint(0,5))
	drawable_image.line(line, fill=(180,180,180,random.randint(100,255)), width = random.randint(1,4), joint='curve')


def draw_curve_line_left(drawable_image):
	step_length = 10
	x1 , y1 =  0, random.randint(0,256)
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




draw_straight_line_top(drawable_image)
draw_straight_line_left(drawable_image)
draw_curve_line_top(drawable_image)
draw_curve_line_left(drawable_image)

draw_straight_line_top(drawable_image)
draw_straight_line_left(drawable_image)
draw_curve_line_top(drawable_image)
draw_curve_line_left(drawable_image)

out = Image.alpha_composite(new_image, base)
converted_out = out.convert("LA")
blured = converted_out.filter(ImageFilter.GaussianBlur(radius=2))
# blured = blured.filter(ImageFilter.SHARPEN)
blured.show()

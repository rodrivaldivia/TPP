import math 
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImagePath

new_image = Image.new("L", (256,256),'#000').convert('RGBA')

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
	drawable_image.line([x1, y1, x2, y2], fill='#fff', width = 1, joint='curve')

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
	drawable_image.line([x1, y1, x2, y2], fill='#fff', width =4, joint='curve')

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
	drawable_image.line(line, fill='#fff', width = 1, joint='curve')


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
		print(angle)
		if(direction == 0):
			angle = angle + abs(random.randint(0,5))
		else:
			angle = angle - abs(random.randint(0,5))
	drawable_image.line(line, fill='#fff', width = 1, joint='curve')

colors=['red','green','yellow','blue','white']

print("Desde Y=0")
# for i in range(3):
# 	x1 , y1 = random.randint(0,256), 0 
# 	line = [ x1, y1 ]
# 	initial_angle = random.randint(0,180)
# 	direction = random.randint(0,1)
# 	angle = initial_angle
# 	x2, y2 = 0, 0
# 	for i in range(40):
# 		angle_sin = np.sin(angle* np.pi / 180)
# 		angle_cos = np.cos(angle* np.pi / 180)
# 		adyacent_cathetus = angle_sin*step_length
# 		oposite_cathetus = angle_cos*step_length
# 		if(angle > 90):
# 			x2 = x1 + oposite_cathetus
# 			y2 = y1 + adyacent_cathetus
# 		else:
# 			x2 = x1 - oposite_cathetus
# 			y2 = y1 + adyacent_cathetus
# 		line.extend([x2,y2])
# 		x1 , y1 = x2, y2
# 		if(direction == 0):
# 			angle = angle + abs(random.randint(0,10))
# 		else:
# 			angle = angle - abs(random.randint(0,10))
# 	drawable_image.line(line, fill='#fff', width = 1, joint='curve')

print("Desde X=0")
# for j in range(5):
# 	x1 , y1 = 0, random.randint(0,256)
# 	angle = random.randint(0,180)
# 	angle_sin = np.sin(angle* np.pi / 180)
# 	angle_cos = np.cos(angle* np.pi / 180)
# 	adyacent_cathetus = angle_sin*line_length
# 	oposite_cathetus = angle_cos*line_length
# 	x2, y2 = 0, 0
# 	if(angle > 90):
# 		x2 = x1 - oposite_cathetus
# 		y2 = y1 - adyacent_cathetus
# 	else:
# 		x2 = x1 + oposite_cathetus
# 		y2 = y1 + adyacent_cathetus
# 	drawable_image.line([x1, y1, x2, y2], fill='#fff', width = 1, joint='curve')
draw_straight_line_top(drawable_image)
draw_straight_line_left(drawable_image)
draw_curve_line_top(drawable_image)
draw_curve_line_left(drawable_image)

out = Image.alpha_composite(new_image, base)

blured = out.filter(ImageFilter.GaussianBlur(radius=2))

out.show()
blured.show()

# from PIL import Image, ImageDraw, ImageFont
# # get an image
# base = Image.new("L", (256,256),'#000').convert('RGBA')

# # make a blank image for the text, initialized to transparent text color
# txt = Image.new('RGBA', base.size, (255,255,255,0))

# # get a font
# # fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)
# # get a drawing context
# d = ImageDraw.Draw(txt)

# # draw text, half opacity
# d.text((10,10), "Hello", fill=(255,255,255,128))
# # draw text, full opacity
# d.text((10,60), "World", fill=(255,255,255,255))

# out = Image.alpha_composite(base, txt)

# out.show()
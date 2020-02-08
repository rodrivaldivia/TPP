import math 
import random
import numpy as np
from PIL import Image, ImageDraw 
from PIL import ImagePath  

new_image = Image.new("L", (256,256),'#000').convert('RGBA')

base = Image.new('RGBA', (256,256), (255,255,255,0))

drawable_image = ImageDraw.Draw(base)


colors=['red','green','yellow','blue','white']

line_length = 400
print("Desde Y=0")
for i in range(5):
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

print("Desde X=0")
for j in range(5):
	x1 , y1 = 0, random.randint(0,256)
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
	drawable_image.line([x1, y1, x2, y2], fill='#fff', width = 1, joint='curve')

out = Image.alpha_composite(new_image, base)

out.show()

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
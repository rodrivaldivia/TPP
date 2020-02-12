import math 
import random
import numpy as np

BOTTOM = 'bottom'
LEFT = 'left'
CHUNK_LENGTH = 20

def polar_to_origin_polar(angle, accumulated_angle, initial_angle):
	angle_to_0 = 45
	angle_to_previous = 135
	angle_with_previous = angle + angle_to_0 +angle_to_previous
	final_angle =  angle_with_previous + accumulated_angle- (180 - initial_angle)
	return final_angle

def polar_to_cartesian(distance, angle, accumulated_angle, initial_angle):
	final_angle = polar_to_origin_polar(angle, accumulated_angle,initial_angle)
	angle_sin = np.sin(final_angle* np.pi / 180)
	angle_cos = np.cos(final_angle* np.pi / 180)
	return distance*angle_cos, distance*angle_sin


class Drawable:

	def __init__(self, position, chunks):
		self.position = position
		self.chunks = chunks
		if(position == BOTTOM):
			x1, y1 = 128 , 256 
			self.initial_angle = 90
		else:
			x1, y1 = 0, 128#random.randint(0,256)
			self.initial_angle = 0#random.randint(-90,90)
		self.initial_position = (x1, y1)
		self.direction = random.randint(0,1)
		coordinates = [[self.initial_position, self.initial_angle]]
		self.movement_index = 0
		for i in range(chunks):
			previous_angle = coordinates[i][1]
			new_angle = 0
			if (self.direction == 0):
				new_angle = random.randint(0,5)
			else:
				new_angle = - random.randint(0,5)
			coordinates.append([(0,0), new_angle])
		self.coordinates = coordinates
		self.wobble_direction = abs(1 - self.direction)

	# def __init__(self,coordinates):
	# 	self.initial_position = coordinates[0], coordinates[1]
	# 	self.chunks = len(coordinates)/2
	# 	self.direction = random.randint(0,1)
	# 	self.movement_index = 0



	def _calculate_angles(self, coordinates):
		points_number = len(coordinates)/2
		coords_list = []
		for i in range(points_number-1):
			x1, y1 = coordinates[(2*i)],coordinates[(2*i)+1]
			x2, y2 = coordinates[(2*(i+1))],coordinates[(2*(i+1))+1]
			width = abs(x2-x1)
			height = abs(y2-y1)
			tang = np.tan(height/width)
			angle = np.arctan(tang) * 180 / np.pi
			coords_list.append([(x1,y1), angle])
		return coords_list


	def _draw_vertical(self):
		x2, y2 = 0, 0
		for index in range(len(self.coordinates)-1):
			angle = self.coordinates[index][1]
			x1, y1 = self.coordinates[index][0]
			angle_sin = np.sin(angle* np.pi / 180)
			angle_cos = np.cos(angle* np.pi / 180)
			oposite_cathetus = angle_sin*CHUNK_LENGTH
			adyacent_cathetus = angle_cos*CHUNK_LENGTH
			if(angle > 0):
				x2 = x1 - oposite_cathetus
				y2 = y1 - adyacent_cathetus
			else:
				x2 = x1 + oposite_cathetus
				y2 = y1 - adyacent_cathetus
			self.coordinates[index+1][0] = (x2,y2)
		coordinates = [ coordinate[0] for coordinate in self.coordinates]
		return [ coordinate for tup in coordinates for coordinate in tup]

	def _draw_horizontal(self):
		x2, y2 = 0, 0
		for index in range(len(self.coordinates)-1):
			angle = self.coordinates[index][1]
			x1, y1 = self.coordinates[index][0]
			angle_sin = np.sin(angle* np.pi / 180)
			angle_cos = np.cos(angle* np.pi / 180)
			oposite_cathetus = angle_sin*CHUNK_LENGTH
			adyacent_cathetus = angle_cos*CHUNK_LENGTH
			if(angle > 0):
				x2 = x1 + adyacent_cathetus
				y2 = y1 - oposite_cathetus
			else:
				x2 = x1 + adyacent_cathetus
				y2 = y1 + oposite_cathetus
			self.coordinates[index+1][0] = (x2,y2)
		coordinates = [ coordinate[0] for coordinate in self.coordinates]
		return [ coordinate for tup in coordinates for coordinate in tup]


	def draw(self):
		x2, y2 = 0, 0
		accumulated_angle = 0
		delta_x, delta_y = polar_to_cartesian(CHUNK_LENGTH, self.coordinates[0][1], accumulated_angle, 0)
		x1, y1 = self.initial_position
		x2 = x1 + delta_x
		y2 = y1 - delta_y
		self.coordinates[1][0] = (x2,y2)
		for index in range(1,len(self.coordinates)-1):
			angle = self.coordinates[index][1]
			x1, y1 = self.coordinates[index][0]
			accumulated_angle += angle	
			delta_x, delta_y = polar_to_cartesian(CHUNK_LENGTH, angle, accumulated_angle, self.initial_angle)
			x2 = x1 + delta_x
			y2 = y1 - delta_y
			self.coordinates[index+1][0] = (x2,y2)
		coordinates = [ coordinate[0] for coordinate in self.coordinates]
		return [ coordinate for tup in coordinates for coordinate in tup]


class SwirlingTubule(Drawable):
	def __init__(self, position, chunks):
		super().__init__(position, chunks)

	def move(self):
		movement_angle = 5
		for index in range(self.movement_index+1):
			previous_angle = self.coordinates[index][1]
			new_angle = 0
			if (self.direction == 0):
				new_angle = previous_angle - 1 * ((index+1 )/ (self.movement_index+1))
			else:
				new_angle = previous_angle + 1 * ((index+1) / (self.movement_index+1))
			self.coordinates[index][1] = new_angle
		if(self.movement_index == self.chunks):
			self.movement_index = 0
			self.direction = abs(1 - self.direction)
		else:
			self.movement_index += 1


class WobblyTubule(Drawable):
	def __init__(self,position, chunks):
		super().__init__(position, chunks)

	def move(self):
		index = self.movement_index
		if (self.wobble_direction == 0):
			self.coordinates[index][1] -= 3
		else:
			self.coordinates[index][1] += 3

		if(self.movement_index == self.chunks):
			self.movement_index = 0
			self.wobble_direction = abs(1 - self.direction)
		else:
			self.movement_index += 1


points_list = []
swirlyLine = SwirlingTubule('bottom', 15)
for i in range(50):
	points = swirlyLine.draw()
	points_list.append(points)
	swirlyLine.move()

from PIL import Image, ImageDraw, ImageFilter, ImagePath

# new_image = Image.new("L", (256,256),'#000').convert('RGBA')
imarray = np.random.rand(256,256,3) * 50
new_image = Image.fromarray(imarray.astype('uint8')).convert('RGBA')
color = (180,180,180,random.randint(100,255))
width = random.randint(1,4)
for i in range(50):
	base = Image.new('RGBA', (256,256), (255,255,255,0))
	drawable_image = ImageDraw.Draw(base)
	drawable_image.line(points_list[i], fill=color, width = width, joint='curve')
	out = Image.alpha_composite(new_image, base)
	converted_out = out.convert("LA")
	blured = converted_out.filter(ImageFilter.GaussianBlur(radius=2))
	blured = blured.filter(ImageFilter.SHARPEN)
	url = 'Video/'+str(i)+'.tif'
	blured.save(url)

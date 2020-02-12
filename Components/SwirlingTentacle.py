import math 
import random
import numpy as np

BOTTOM = 'bottom'
LEFT = 'left'
CHUNK_LENGTH = 10

# def nextPointInCartesian(start_coord, end_coord, angle, length):


class SwirlingTentacle:

	def __init__(self, position, chunks):
		self.position = position
		self.chunks = chunks
		if(position == BOTTOM):
			x1, y1 = random.randint(0,256) , 256 
		else:
			x1, y1 = 0, random.randint(0,256)
		self.initial_position = (x1, y1)
		self.direction = random.randint(0,1)
		self.initial_angle = random.randint(-90,90)
		coordinates = [[self.initial_position, self.initial_angle]]
		self.direction = random.randint(0,1)
		self.movement_index = 0
		for i in range(chunks):
			previous_angle = coordinates[i][1]
			new_angle = 0
			if (self.direction == 0):
				new_angle = previous_angle +  abs(random.randint(0,5))
			else:
				new_angle = previous_angle -  abs(random.randint(0,5))
			coordinates.append([(0,0), new_angle])
		self.coordinates = coordinates
		self.wobble_direction = abs(1 - self.direction)

		



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
		if(self.position == BOTTOM):
			return self._draw_vertical()
		else:
			return self._draw_horizontal()

	def swirl(self):
		movement_angle = 5
		for index in range(self.movement_index+1):
			previous_angle = self.coordinates[index][1]
			new_angle = 0
			if (self.direction == 0):
				new_angle = previous_angle - 1
			else:
				new_angle = previous_angle + 1
			self.coordinates[index][1] = new_angle
			if(self.movement_index == self.chunks):
				self.movement_index = 0
			else:
				self.movement_index += 1

	def wobble(self):
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




swirlyLine = SwirlingTentacle('bottom', 40)
points = swirlyLine.draw()
for i in range(40):
	swirlyLine.swirl()
points2 = swirlyLine.draw()
for i in range(40):
	swirlyLine.swirl()
points3 = swirlyLine.draw()
for i in range(40):
	swirlyLine.swirl()
points4 = swirlyLine.draw()
swirlyLine2 = SwirlingTentacle('left', 40)
points5 = swirlyLine2.draw()
print(points5)
for i in range(40):
	swirlyLine2.wobble()
points6 = swirlyLine2.draw()
for i in range(40):
	swirlyLine2.wobble()
points7 = swirlyLine2.draw()
for i in range(40):
	swirlyLine2.wobble()
points8 = swirlyLine2.draw()

from PIL import Image, ImageDraw, ImageFilter, ImagePath

# new_image = Image.new("L", (256,256),'#000').convert('RGBA')
imarray = np.random.rand(256,256,3) * 50
new_image = Image.fromarray(imarray.astype('uint8')).convert('RGBA')

base = Image.new('RGBA', (256,256), (255,255,255,0))

drawable_image = ImageDraw.Draw(base)
drawable_image.line(points, fill=(180,180,180,random.randint(100,255)), width = random.randint(1,4), joint='curve')
drawable_image.line(points2, fill=(180,180,180,random.randint(100,255)), width = random.randint(1,4), joint='curve')
drawable_image.line(points3, fill=(180,180,180,random.randint(100,255)), width = random.randint(1,4), joint='curve')
drawable_image.line(points4, fill=(180,180,180,random.randint(100,255)), width = random.randint(1,4), joint='curve')
drawable_image.line(points5, fill=(180,180,180,random.randint(100,255)), width = random.randint(1,4), joint='curve')
drawable_image.line(points6, fill=(180,180,180,random.randint(100,255)), width = random.randint(1,4), joint='curve')
drawable_image.line(points7, fill=(180,180,180,random.randint(100,255)), width = random.randint(1,4), joint='curve')
drawable_image.line(points8, fill=(180,180,180,random.randint(100,255)), width = random.randint(1,4), joint='curve')
out = Image.alpha_composite(new_image, base)
converted_out = out.convert("LA")
blured = converted_out.filter(ImageFilter.GaussianBlur(radius=2))
blured = blured.filter(ImageFilter.SHARPEN)
blured.show()
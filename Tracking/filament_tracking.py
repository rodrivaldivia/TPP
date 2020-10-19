import filament_init, points_corrector
from PIL import Image, ImageDraw
from os import listdir
from os.path import isfile, join

imgFolder = 'Images/canal_1/'
images = [f for f in listdir(imgFolder) if isfile(join(imgFolder, f)) and f.endswith(".tif")]
images.sort()

# print(images)


# filamentPoints = filament_init.create(images[0])
# filamentPoints = [(159, 24), (164, 28), (170, 32), (176, 39), (182, 45), (189, 51), (196, 57), (203, 64), (210, 71), (217, 79)]
filamentPoints = [(98, 211), (103, 196), (109, 184), (114, 173), (118, 161), (124, 146), (124, 147), (129, 132), (136, 119), (141, 107)]

# print(filamentPoints);


# original = Image.open('Images/canal_1/s_C001T001.tif')
for imagePath in images:
	im = Image.open(imgFolder + imagePath)

	filamentPoints = points_corrector.correctPoints(im, filamentPoints)
	newPoints = []
	for t in filamentPoints:
		lst = list(t)
		lst[0] = int(lst[0])
		lst[1] = int(lst[1])
		t = tuple(lst)
		newPoints.append(t)

	filamentPoints = newPoints
	
	im = im.point(lambda i:i*(1./256)).convert('RGB')


	drawable_image = ImageDraw.Draw(im)
	# drawable_image.line(coordenates, fill='#00ff00', width = 5, joint='curve')
	drawable_image.line(filamentPoints, fill='#ff00ff', width = 5, joint='curve')
	# im.show()
	im.save('Images/results/' + imagePath)

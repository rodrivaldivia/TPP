import filament_init, points_corrector
from PIL import Image, ImageDraw

coordenates = [(23, 15), (41, 30), (56, 43), (72, 59), (90, 73), (110, 87), (126, 104), (148, 126), (167, 142), (185, 168)]
# coordenates = filament_init.create()
# print(coordenates);


im = Image.open('Images/canal_1/s_C001T001.tif')
# for (all images):
# 	new_points = points_corrector
points_corrector.correctPoints(im, coordenates)

# im = im.point(lambda i:i*(1./256)).convert('RGB')

# drawable_image = ImageDraw.Draw(im)
# drawable_image.line(coordenates, fill='#00ff00', width = 5, joint='curve')
# im.show()

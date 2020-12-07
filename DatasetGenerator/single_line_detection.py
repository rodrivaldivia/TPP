from PIL import Image
import numpy as np

im = Image.open("./train/s_C001T015.tif")

a = np.array(im)

print(a.shape)
print(a[25])
a[0][0] = 3
print(a[0])
print(a[2])
a[25] = np.zeros(256) + 255
a[26] = np.zeros(256) + 255
a[27] = np.zeros(256) + 255
print(a[24: 27])

b = Image.fromarray(a)

b.rotate(45).show()
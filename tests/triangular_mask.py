import numpy as np
from PIL import Image

def triangular_mask(img_width, img_height, mask_angle):
    x, y = np.ogrid[:img_width, :img_height]
    distance_field = np.abs(mask_angle * (y - int(0.5*img_width)))
    triangular_mask = (distance_field >= (x - int(0.5*img_height))) & (~distance_field <= (x - int(0.5*img_height)))
    return triangular_mask

img_width, img_height, mask_angle = 9, 9, 2
mask = triangular_mask(img_width, img_height, mask_angle)

im = Image.fromarray(mask)
im.show()
print(mask)

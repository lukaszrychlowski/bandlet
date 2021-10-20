import numpy as np
import maths
from PIL import Image

def triangular_mask(img_width, img_height, mask_angle):
    x, y = np.ogrid[:img_width, :img_height]
    distance_field = np.abs(mask_angle * (x - round(0.5*img_width, ndigits=None)))
    triangular_mask = (distance_field >= (y - round(0.5*img_height, ndigits=None))) & (~distance_field <= (y - round(0.5*img_height, ndigits=None)))
    return triangular_mask

img_width, img_height, mask_angle = 9, 9, 2
mask = triangular_mask(img_width, img_height, mask_angle)

im = Image.fromarray(mask)
im.show()
print(mask)

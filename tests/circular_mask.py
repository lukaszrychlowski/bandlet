import numpy as np
from PIL import Image

def circular_mask(img_width, img_height, mask_radius):
    x, y = np.ogrid[:img_width, :img_height]
    distance_field = np.sqrt((x - round(0.5*img_width, ndigits=None))**2 + 
                             (y - round(0.5*img_height, ndigits=None))**2)
    circular_mask = distance_field <= mask_radius
    return circular_mask

img_width, img_height, radius = 100,100,30
mask = circular_mask(img_width, img_height, radius)

im = Image.fromarray(mask)
im.show()
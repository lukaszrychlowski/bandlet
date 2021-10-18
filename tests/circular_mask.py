import numpy as np

def circular_mask(img_width, img_height, mask_radius):
    x, y = np.ogrid[:img_width, :img_height]
    distance_field = np.sqrt((x - round(0.5*img_width, ndigits=None))**2 + (y-round(0.5*img_height, ndigits=None))**2)
    print(distance_field)
    circular_mask = distance_field <= mask_radius
    return circular_mask

img_width, img_height, radius = 8,8,2
mask = circular_mask(img_width, img_height, radius)
print(mask)
from warnings import catch_warnings
import numpy as np
from numpy.core.fromnumeric import trace
import maths
from PIL import Image

''' returns false if px is inside a mask '''
def triangular_mask(img_width, img_height, mask_angle):
    x, y = np.ogrid[:img_width, :img_height]
    distance_field = np.abs(mask_angle * (x - round(0.5*img_width, ndigits=None)))
    triangular_mask = (distance_field >= (y - round(0.5*img_height, ndigits=None))) & (~distance_field <= (y - round(0.5*img_height, ndigits=None)))
    return triangular_mask

img_width, img_height, mask_angle = 200, 200, 10
angle = 22
mask = triangular_mask(img_width, img_height, mask_angle)

def rotation(img_width, img_height, rotation_angle):
    rotation_matrix = maths.rotation_matrix(rotation_angle)
    translation_matrix = maths.translation_matrix(img_width, img_height)
    reverse_translation_matrix = maths.reverse_translation_matrix(img_width, img_height)
    rotated_triangular_mask = np.ones((img_width, img_height), dtype=bool)
    for i in range(img_width):
        for j in range(img_height):
            if triangular_mask[i,j] == False:
                pixel_pos = np.array([i,j,1])
                rotated_pixel_pos = maths.array_rotation(pixel_pos, translation_matrix, rotation_matrix, reverse_translation_matrix)
                rotated_pixel_pos = np.rint(rotated_pixel_pos)
                rotated_pixel_pos = rotated_pixel_pos.astype(int)
                rotated_triangular_mask[rotated_pixel_pos[0], rotated_pixel_pos[1]] = triangular_mask[i,j]
                
    for k in range(img_width-1):
        for l in range(img_height-1):
            if (rotated_triangular_mask[k+1,l] == False & rotated_triangular_mask[k-1,l] == False):
                rotated_triangular_mask[k,l] = False

    return rotated_triangular_mask

rotated_mask = rotation(img_width, img_height, angle)
im = Image.fromarray(rotated_mask)
im.show()

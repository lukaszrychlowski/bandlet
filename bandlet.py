import numpy as np
from matplotlib import pyplot as plt
import maths
from PIL import Image 

''' Generate the image array based on data from path, get its size. '''
path = '/Users/ryszard/Desktop/pattern_fcc_02.txt'
#path = '/Users/user/Desktop/pattern_fcc_02.txt'
img = np.genfromtxt(path, deletechars='.000')
img_width, img_height = img.shape

''' Fast fourier transform is applied to the img. The zero frequency
    is shifted to the center of the img in order to make masking easier. 
    Log of abs ft values is used only for displaying the spectrum. '''
ft = np.fft.fft2(img)
ft = np.fft.fftshift(ft)
ft_img = np.log10(np.abs(ft))

''' Used to mask frequencies in the ft. Creates boolean array of image size.
    It's a simple distance field check - if the image[i,j] is inside the area 
    of defined circle it returns boolean_mask[i,j] = False. '''
def circular_mask(img_width, img_height, mask_radius):
    x, y = np.ogrid[:img_width, :img_height]
    distance_field = np.sqrt((x - round(0.5*img_width, ndigits=None))**2 + 
                             (y - round(0.5*img_height, ndigits=None))**2)
    circular_mask = distance_field <= mask_radius
    return circular_mask
def triangular_mask(img_width, img_height, mask_angle):
    x, y = np.ogrid[:img_width, :img_height]
    distance_field = np.abs(mask_angle * (x - round(0.5*img_width, ndigits=None)))
    triangular_mask = (distance_field >= (y - round(0.5*img_height, ndigits=None))) & (~distance_field <= (y - round(0.5*img_height, ndigits=None)))
    return triangular_mask

''' Rotates the triangular mask by given angle. Method iterates over the mask array
    and checks the bool value, if given coordinate (x,y) belongs to a masked area it 
    is transformed by rotation to (x',y'). Calculated px coords are most often subpixel values, 
    they're rounded to int. It creates holes inside a mask, so another iteration over array is done 
    to fill the gaps. '''
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

'''Create both mask arrays with given array size and angle/radius, make a copy of img and apply masks to it.'''
triangular_mask = triangular_mask(img_width, img_height, 10)
circular_mask = circular_mask(img_width, img_height, 20)

rotated_triangular_mask = rotation(img_width, img_height, 25)
masked_img = np.copy(img)
masked_img[rotated_triangular_mask] = 0
masked_img[circular_mask] = 0

im = Image.fromarray(masked_img)
im.show()


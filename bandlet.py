import numpy as np
from matplotlib import pyplot as plt
import maths

''' Generate the image array, get its size '''

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

''' Used to mask lower frequencies in the ft. Creates boolean array of image size.
    It's a simple distance field check - if the image[i,j] is inside the area 
    of defined circle it returns boolean_mask[i,j] = False '''

def circular_mask(img_width, img_height, mask_radius):
    x, y = np.ogrid[:img_width, :img_height]
    distance_field = np.sqrt((x - round(0.5*img_width, ndigits=None))**2 + 
                             (y - round(0.5*img_height, ndigits=None))**2)
    circular_mask = distance_field >= mask_radius
    return circular_mask

''' Mask frequencies in ft space, returns False for pixels inside the mask '''

def triangular_mask(img_width, img_height, mask_angle):
    x, y = np.ogrid[:img_width, :img_height]
    distance_field = np.abs(mask_angle * (y - int(0.5*img_width)))
    triangular_mask = (distance_field >= (x - int(0.5*img_height))) & (~distance_field <= (x - int(0.5*img_height)))
    return triangular_mask
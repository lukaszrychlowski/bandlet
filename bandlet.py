import numpy as np
from matplotlib import pyplot as plt

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
    of defined circle it returns boolean_mask[i,j] = True '''

def circular_mask(img_width, img_height, mask_radius):
    x, y = np.ogrid[:img_width, :img_height]
    distance_field = np.sqrt((x - round(0.5*img_width, ndigits=None))**2 + 
                             (y - round(0.5*img_height, ndigits=None))**2)
    circular_mask = distance_field <= mask_radius
    return circular_mask

def triangular_mask(img_width, img_height, mask_angle):
    x, y = np.ogrid[:img_width, :img_height]
    distance_field = np.abs(mask_angle * (x - round(0.5*img_width, ndigits=None)))
    triangular_mask = (distance_field >= (y - round(0.5*img_height, ndigits=None)) & 
                      (~distance_field <= (y - round(0.5*img_height, ndigits=None)))
    return triangular_mask
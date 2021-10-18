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

def circular_mask(img_width, img_height, mask_radius):
    x, y = np.ogrid[:img_width, :img_height]
    distance_field = np.sqrt((x - round(0.5*img_width, ndigits=None))**2 + (y-round(0.5*img_height, ndigits=None))**2)
    print(distance_field)
    circular_mask = distance_field <= mask_radius
    return circular_mask

img_width, img_height, radius = 8,8,2
mask = circular_mask(img_width, img_height, radius)
print(mask)
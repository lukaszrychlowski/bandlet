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
    y, x = np.ogrid[:img_width, :img_height]
    distance_field = np.abs(mask_angle * (x - round(0.5*img_height, ndigits=None)))
    triangular_mask = (distance_field >= (y - round(0.5*img_width, ndigits=None))) & (~distance_field <= (y - round(0.5*img_width, ndigits=None)))
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

    ## for every px in array
    for i in range(img_width):
        for j in range(img_height):
            ## check if px is inside a mask
            if triangular_mask[i,j] == False:
                ## if it is, get its position
                pixel_pos = np.array([i,j,1])
                ## rotate its coordinates to new position and round to int value
                rotated_pixel_pos = maths.array_rotation(pixel_pos, translation_matrix, rotation_matrix, reverse_translation_matrix)
                rotated_pixel_pos = np.rint(rotated_pixel_pos)
                rotated_pixel_pos = rotated_pixel_pos.astype(int)
                ## check if rotated px coordinate is within array, if not - skip it
                if rotated_pixel_pos[0] < img_width and rotated_pixel_pos[1] < img_height:
                    rotated_triangular_mask[rotated_pixel_pos[0], rotated_pixel_pos[1]] = triangular_mask[i,j]
                else:
                    continue

    ## fill voids inside a mask
    for k in range(img_width-1):
        for l in range(img_height-1):
            if (rotated_triangular_mask[k+1,l] == False & rotated_triangular_mask[k-1,l] == False):
                rotated_triangular_mask[k,l] = False

    return rotated_triangular_mask

'''Create both mask arrays with given array size and angle/radius, make a copy of img and apply masks to it.'''
triangular_mask = triangular_mask(img_width, img_height, 10)
circular_mask = circular_mask(img_width, img_height, 10)

rotation_angle = 45

rotated_triangular_mask = rotation(img_width, img_height, rotation_angle)
masked_ft = np.copy(ft_img)
masked_ft[rotated_triangular_mask] = 0
masked_ft[circular_mask] = 0
print(img.shape)
print(triangular_mask.shape)
print(rotated_triangular_mask.shape)
#im = Image.fromarray(masked_ft)
#im.show()
plt.imshow(masked_ft)
plt.show()


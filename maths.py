import numpy as np

def array_rotation(array, translation_matrix, rotation_matrix, reverse_translation_matrix):
    return translation_matrix @ rotation_matrix @ reverse_translation_matrix @ array

def translation_matrix(img_width, img_height):
    return np.array(
            [
                [1, 0, img_width/2],
                [0, 1, img_height/2],
                [0, 0, 1]
            ])

def reverse_translation_matrix(img_width, img_height):
    return np.array(
            [
                [1, 0, -img_width/2],
                [0, 1, -img_height/2],
                [0, 0, 1]
            ])

def rotation_matrix(angle_degree):
    angle_radians = np.radians(angle_degree)
    sin = np.sin(angle_radians)
    cos = np.cos(angle_radians)

    return np.array(
            [
                [cos, sin, 0],
                [-sin, cos, 0],
                [0, 0, 1]
            ])
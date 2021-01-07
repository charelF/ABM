from cairosvg import svg2png
from PIL import Image
import numpy as np
from numba import njit

DATA_PATH = '../data/'

def get_svg_data(filename):
    """
    Given filename reutnrs the data in that file
    """
    with open(filename, 'r') as file:
        data = file.read().replace('\n', '')
        return data

def convert_svg_to_png(svg_code, output_name):
    """
    return png object from svg code
    """
    return svg2png(bytestring=svg_code,write_to=output_name)

def get_non_zero_pixels(im_as_array):
    """
    Returns set of non-zero elemnts in array
    """
    vertical_translation = im_as_array.shape[0]
    land_pixels = []
    for i, vertical in enumerate(im_as_array):
        for j, horizontal in enumerate(vertical):
            for rgb_val in horizontal:
                if rgb_val != 0:
                    land_pixels.append((j, vertical_translation - i))
                    
    return set(land_pixels)

if __name__ == '__main__':
    output = DATA_PATH + 'output.png'
    data = get_svg_data(DATA_PATH + 'europe.svg')
    convert_svg_to_png(data, output)
    im = Image.open(output)
    im_as_array = np.asarray(im)
    land_pixels = get_non_zero_pixels(im_as_array)

    import matplotlib.pyplot as plt
    x , y = zip(*land_pixels)
    #plt.scatter(x, y, s = 0.1)
    #plt.show()
    np.savetxt(DATA_PATH + 'europe_array.txt', np.column_stack((x, y)), fmt = '(%i, %i)')

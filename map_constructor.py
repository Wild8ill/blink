#!/usr/bin/python3

from PIL import Image
import sys
from objects import *
from colormap import rgb2hex

class MapConstructor:
    def __init__(self,HEIGHT):
        self.HEIGHT = HEIGHT


    def generate_pixel_array(self, size):
        temp_array = [x for x in range(size)]
        for index in temp_array:
            temp_array[index] = [False for x in range(size)]
        print(temp_array)
        return temp_array


    def return_obj_array(self, filename):
        object_array = []
        try:
            map = Image.open(filename)

        except IOError:
            print("Unable to load image")
            sys.exit(1)

        pixel_matrix = self.generate_pixel_array(map.size[0])
        rgb_map = map.convert("RGB")
        for column in range(map.size[0]):
            for row in range(map.size[1]):
                r, g, b = rgb_map.getpixel((row, column))
                pixel_matrix[row][column] = True
                if r != 255 or g != 255 or b != 255:
                    hexval = rgb2hex(r,g,b)
                    object_array.append(self.object_type(hexval,(row,column)))
        return object_array

    def object_type(self, hexval,*arg):
        X = arg[0][0] * 16
        Y = arg[0][1] * 16
        print(X,Y)

        # a 32 pixel wide sprite should be 16 pixels across
        object_dict = {
            "#000000":Platform(),
            "#570000":FloatingPlatform(X,32,Y)
            #"#00e9e5":Player(Vector((X,Y)))
        }
        return object_dict.get(hexval)
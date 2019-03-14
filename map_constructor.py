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
        return temp_array


    def generate_map(self, filename):
        object_array = []
        try:
            map = Image.open(filename)

        except IOError:
            print("Unable to load image")
            sys.exit(1)

        pixel_matrix = self.generate_pixel_array(map.size[0])
        print(map.size)
        rgb_map = map.convert("RGB")
        for column in range(map.size[0]):
            for row in range(map.size[1]):
                r, g, b = rgb_map.getpixel((row, column))
                pixel_matrix[row][column] = True
                if r != 255 or g != 255 or b != 255:
                    hexval = rgb2hex(r,g,b)
                    object_to_add = self.object_type(hexval,(row,column))

                    if object_to_add is not None:
                        print(type(object_to_add),hexval)
                        object_array.append(object_to_add)
        return object_array


    def object_type(self, hexval,*arg):
        X = arg[0][0] * 16
        Y = arg[0][1] * 16
        hexval = hexval.lower()
        # a 32 pixel wide sprite should be 16 pixels across
        object_dict = {
            "#000000":Platform(),
            "#570000":FloatingPlatform(X,32,Y),
            "#00e9e5":Player(Vector((X,Y)),Vector((0,0)),32,IMG,9,5)
        }
        return object_dict.get(hexval)
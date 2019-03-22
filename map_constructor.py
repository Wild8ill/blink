#!/usr/bin/python3

from PIL import Image
import sys
from platforms import *
from items import *
from entity import *
from colormap import rgb2hex

class MapConstructor:
    def __init__(self,WIDTH,HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.player_pos = (0,0)
        self.PLAYER = None
        self.final_array = []

    def generate_pixel_array(self, size):
        temp_array = [x for x in range(size)]
        for index in temp_array:
            temp_array[index] = [False for x in range(size)]
        return temp_array


    def generate_map(self, filename):
        if filename == "levels/welcome_screen":
            return [HomeScreen(self.WIDTH/2, self.HEIGHT/2)]

        object_array = []
        try:
            map = Image.open(filename)

        except IOError:
            print("Unable to load image")
            sys.exit(1)

        pixel_matrix = self.generate_pixel_array(map.size[0])
        rgb_map = map.convert("RGB")

        for column in range(map.size[0]):  # iterate through and find the index of the player. Used to calculate relative positions
            for row in range(map.size[1]):
                r, g, b = rgb_map.getpixel((row, column))
                hexval = rgb2hex(r,g,b)
                if hexval.lower() == "#00e9e5":
                    self.player_pos = (row,column)
                    self.PLAYER = self.object_type(hexval,(row,column))
                    #object_array.append(self.PLAYER)
                    break # break for efficiency

        for column in range(map.size[0]): # yay we're iterating again this seems efficient
            for row in range(map.size[1]):
                r, g, b = rgb_map.getpixel((row, column))
                pixel_matrix[row][column] = True
                if r != 255 or g != 255 or b != 255:
                    hexval = rgb2hex(r,g,b)
                    object_to_add = self.object_type(hexval,(row,column))

                    if object_to_add is not None:
                        object_array.append(object_to_add)
                        self.final_array.append(object_to_add) # allows us to update positions of everything except excalibur
        self.update_positions
        return object_array


    def object_type(self, hexval,*arg):
        X = arg[0][0] * 16
        Y = arg[0][1] * 16
        X = arg[0][0] * 32
        Y = arg[0][1] * 32

        hexval = hexval.lower()
        # a 32 pixel wide sprite should be 16 pixels across
        object_dict = {
            "#000000":Platform(),
            "#570000":FloatingPlatform(X,Y,32),
            "#00e9e5":Player(Vector((X, Y)), Vector((0, 0)), 32, IMG, 9, 5, self.WIDTH, self.HEIGHT, self),
            "#002657":Blip(X,Y,1),
            "#fff100": Heart(X, Y),
            "#2d0b0b":GameOverScreen(X,Y,self.WIDTH,self.HEIGHT),
            "#132d0b":HomeScreen(X, Y, self.WIDTH, self.HEIGHT),
        }
        return object_dict.get(hexval)

    def update_positions(self):
        for object in self.final_array:
            object.relative_pos = object.pos.copy() + self.PLAYER.vector_transform
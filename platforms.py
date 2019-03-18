try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import *
from sprite import *
from util import *
from abc import ABC, abstractmethod

IMG = 'https://i.postimg.cc/7L7LYWTC/blink-sprites.png'

#############################################################################################
# Platform
class Platform:
    def __init__(self, x=400, y=400):
        self.y = y
        self.x = x
        self.border = 1
        self.color = "red"
        self.sprite = Sprite(IMG, 9, 6)
        self.pos = Vector((x, y))
        self.relative_pos = self.pos.copy()
        self.block_width = 16

    def draw(self, canvas):
        self.sprite.draw(canvas, self.relative_pos, (self.block_width, self.block_width), [0, 5])
        #for line in self.return_hitbox():
        #    line.draw(canvas)

    def return_hitbox(self):  # method to return 4 lines defining the outer bounds of the block
        midpoint = self.relative_pos
        half_width = self.block_width / 2

        # define edges
        left = midpoint.x - half_width
        right = midpoint.x + half_width
        top = midpoint.y - half_width
        bottom = midpoint.y + half_width

        # define points
        upper_left = Vector((left, top))
        upper_right = Vector((right, top))
        lower_left = Vector((left, bottom))
        lower_right = Vector((right, bottom))

        # define lines
        left_edge = Line(lower_left, upper_left)
        top_edge = Line(upper_left, upper_right)
        right_edge = Line(upper_right, lower_right)
        bottom_edge = Line(lower_right, lower_left)

        return (left_edge, top_edge, right_edge, bottom_edge)

class FloatingPlatform(Platform):
    def __init__(self, x, y=400, width=0):
        self.y = y
        self.x = x
        self.width = width
        super().__init__(x, y)
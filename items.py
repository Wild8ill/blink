try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import *
from sprite_sheet import *
from util import *

class Item:
    def __init__(self, x, y, sprite_progression=[0],radius=16):
        self.x = x
        self.y = y
        self.radius = radius
        self.pos = Vector((x,y))
        self.relative_pos = self.pos
        self.sprite_progression = sprite_progression
        #self.sprite = Sprite(IMG, 9, 6)
        self.sprite = Sprite_Sheet()
        self.current_sprite = 0

    def draw(self,canvas):
        #self.sprite.draw(canvas, self.relative_pos, (self.radius*2, self.radius*2), [self.sprite_progression[self.current_sprite], self.sprite.frame_index[1]])
        self.sprite.draw(canvas, self.relative_pos, (self.radius*2, self.radius*2), [0,7])
        self.current_sprite %= len(self.sprite_progression)
        self.current_sprite += 1

    def return_hitbox(self):  # method to return 4 lines defining the outer bounds of the block
        midpoint = self.relative_pos
        half_width = self.radius

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


class Heart(Item):
    def __init__(self,x,y):
        self.sprite_progression = [0,1,2,3,4,5,6]
        super().__init__(x,y, self.sprite_progression)
        self.value = 0.5
        self.sprite = Sprite_Sheet()

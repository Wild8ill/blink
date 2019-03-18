try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import *
from sprite import *
from util import *
from platforms import *
from abc import ABC, abstractmethod

IMG = 'https://i.postimg.cc/7L7LYWTC/blink-sprites.png'

<<<<<<< HEAD:objects.py

#############################################################################################
# Platform
class Block:
    #wow generic class to contain all types of blocks
    def __init__(self, x=400, y=400):
        self.y = y
        self.border = 1
        self.normal = Vector((0, 1))
        self.edgeR = y + 1 + self.border
        self.sprite = Sprite(IMG, 9, 6)
        self.pos = Vector((x, y))
        self.relative_pos = self.pos.copy()
        self.block_width = 16

class Platform(Block):
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

class Spike(Block):
    pass
=======
>>>>>>> 4-Documentation:entity.py
#############################################################################################
# Player
class Entity: # base class that encompasses players and enemies
    def collide(self):
        pass

class Player(Entity):  # model the character as a ball for now convenient hitboxes
    def __init__(self, pos=Vector((0, 0)), vel=Vector((0, 0)), radius=32, image=IMG, columns=1, row=1, width=0,
                 height=0, map=None):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.diameter = radius * 2
        self.border = 1
        self.sprite = Sprite(image, columns, row)
        self.move_buffer = []
        self.collision = []
        self.state = "rest"
        self.animation_frame = 0
        self.WIDTH = width
        self.HEIGHT = height
        self.MAP = map
        self.vector_transform = Vector((self.WIDTH / 2, self.HEIGHT / 2)) - self.pos
        self.terminal_vel = 2
        self.level_finished = False
        self.relative_pos = Vector((width/2,height/2))

    # def offsetB(self):
    #     return self.pos.y + self.radius

    def update(self, clock):
        if self.level_finished:
            return "Next Level"
        self.pos.add(self.vel)
        self.vel.subtract(Vector((0, -0.0981)))
        self.MAP.update_positions()  # calculates all relative positions for objects, now that player is set up properly


        # State Checking
            # What Sprite do we
        if self.state == "rest":
            self.sprite.set_frame([0, 0])
            for move in self.move_buffer:
                self.handle_move(move)

        elif self.state == "attack":
            self.sprite.set_frame([0, 0])
            if clock.return_mod(2):
                self.sprite.step_frame()
                self.animation_frame += 1
            self.move_right(1)
            if self.animation_frame == 9:
                self.animation_frame = 0
                self.state = "rest"
                self.remove_move("a")

        elif self.state == "blink":
            if clock.return_mod(10):
                print("change")
                self.sprite.step_frame()
                self.animation_frame += 1
            if self.animation_frame == 9:
                self.animation_frame = 0
                self.state = "rest"
                self.remove_move("s")
        self.vector_transform = Vector((self.WIDTH / 2, self.HEIGHT / 2)) - (self.pos)
        self.check_collision()

    def draw(self, canvas):
        canvas.draw_circle((self.WIDTH / 2, self.HEIGHT / 2),
                           self.radius,
                           1,
                           "blue",
                           "blue")
        self.sprite.draw(canvas, Vector((self.WIDTH / 2, self.HEIGHT / 2)), (self.diameter, self.diameter))

##################################################################
# Player Move Handling

    def add_move(self, key):
        self.move_buffer.append(key)

    def remove_move(self, key):
        for key in self.move_buffer:
            self.move_buffer.remove(key)

    def handle_move(self, move):
        if move == simplegui.KEY_MAP["left"]:
            self.move_left(3)
        if move == simplegui.KEY_MAP["up"]:
            self.jump()
            self.remove_move(move)
        if move == simplegui.KEY_MAP["right"]:
            self.move_right(3)
        if move == simplegui.KEY_MAP["a"]:
            self.__setstate__("attack")
        if move == simplegui.KEY_MAP["s"]:
            self.__setstate__("blink")
        if move == simplegui.KEY_MAP["e"]:
            self.level_finished = True

    def move_left(self, speed):
        if self.vel.x < self.terminal_vel:
            self.vel.add(Vector((-speed, 0)))

    def move_right(self, speed):
        if self.vel.x < self.terminal_vel:
            self.vel.add(Vector((speed, 0)))

    def jump(self, type="single"):
        self.vel.add(Vector((0, -3)))

    def __setstate__(self, state):
        self.state = state

    def collide(self):
        self.vel = Vector((0,0))
        pass

    def check_collision(self):
        if len(self.collision) != 0:
            for object in self.collision:
                if isinstance(object, Platform):
                    self.vel.y = 0
                    self.pos.y = object.y - self.radius


#################################################
# ENEMY

class Enemy(Entity):
    def __init__(self, x, y, sprite_progression=[0],radius=16):
        self.x = x
        self.y = y
        self.radius = radius
        self.pos = Vector((x,y))
        self.relative_pos = self.pos
        self.sprite_progression = sprite_progression
        self.sprite = Sprite(IMG, 9, 6)

    def draw(self,canvas):
        self.sprite.draw(canvas, self.relative_pos, (self.radius*2, self.radius*2), [0, 4])

class Blip(Enemy):
    def __init__(self, x, y, velocity):
        self.vel = Vector((0,velocity))
        self.sprite_progression = [1, 2, 1, 4]
        super().__init__(x, y, self.sprite_progression)

    def update(self):
        print("I am updating")
        self.pos += self.vel

    def collide(self):
        self.vel.reflect(Vector((0,-1)))



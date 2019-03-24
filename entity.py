try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import *
from sprite import *
from util import *
from platforms import *
from abc import ABC, abstractmethod

#############################################################################################
# Player
class Entity: # base class that encompasses players and enemies
    def collide(self):
        pass

class Player(Entity):  # model the character as a ball for now convenient hitboxes
    def __init__(self, pos=Vector((0, 0)), vel=Vector((0, 0)), radius=32, columns=1, row=1, width=0,height=0, map=None):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.diameter = radius * 2
        self.border = 1
        self.sprite = Sprite_Sheet([0,3])
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
        self.direction = "right"

        self.clock = Clock()

    # def offsetB(self):
    #     return self.pos.y + self.radius

    def update(self):
        if self.level_finished:
            return "Next Level"

        self.pos.add(self.vel)

        # Removing X Velocity over time 
            # Removes 1/2 each loop 
            # When at less than 0.1 set to 0
        if (self.vel.x > 0):
            if(self.vel.x < 0.1):
                self.vel.subtract(Vector((self.vel.x, 0)))
            else: 
                tmpx = self.vel.x / 2
                self.vel.subtract(Vector((tmpx, 0)))

        # Adds some "Gravity"
        self.vel.subtract(Vector((0, -0.0981)))

        self.MAP.update_positions()  # calculates all relative positions for objects, now that player is set up properly

        # State Checking
            # What Sprite do we
        if self.state == "rest":
            if self.direction == "right":
                self.sprite.set_frame([0, 3])
            else:
                self.sprite.set_frame([4,2])

            for move in self.move_buffer:
                self.handle_move(move)

        elif self.state == "attack":
            if self.direction == "right":
                self.sprite.set_frame([0, 0])
            else:
                self.sprite.set_frame([8,1])

            if self.clock.return_mod(5):
                self.sprite.step_frame()
                self.animation_frame += 1
            self.move_right(1)
            if self.animation_frame == 8:
                self.animation_frame = 0
                self.state = "rest"
                self.remove_move("a")

        elif self.state == "blink":
            if self.clock.return_mod(10):
                self.sprite.step_frame()
                self.animation_frame += 1
            if self.animation_frame == 8:
                self.animation_frame = 0
                self.state = "rest"
                self.remove_move("s")
        self.vector_transform = Vector((self.WIDTH / 2, self.HEIGHT / 2)) - (self.pos)
        self.clock.increment_clock

    def draw(self, canvas):
        # canvas.draw_circle((self.WIDTH / 2, self.HEIGHT / 2),
        #                    self.radius,
        #                    1,
        #                    "blue",
        #                    "blue")
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
        self.direction = "left"
        if math.fabs(self.vel.x) < self.terminal_vel:
            self.vel.add(Vector((-speed, 0)))

    def move_right(self, speed):
        self.direction = "right"
        if math.fabs(self.vel.x) < self.terminal_vel:
            self.vel.add(Vector((speed, 0)))

    def jump(self, type="single"):
        self.vel.add(Vector((0, -3)))

    def __setstate__(self, state):
        self.state = state

    def collide(self):
        # self.vel.reflect(Vector((0,-1)))
        self.vel = Vector((0,0))
        self.pos.y -= 0.1
        pass


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
        #self.sprite = Sprite(IMG, 9, 6)
        self.sprite = Sprite_Sheet()

    def draw(self,canvas):
        self.sprite.draw(canvas, self.relative_pos, (self.radius*2, self.radius*2), [0, 4])

class Blip(Enemy):
    def __init__(self, x, y, velocity):
        self.vel = Vector((0,velocity))
        self.sprite_progression = [1, 2, 1, 4]
        super().__init__(x, y, self.sprite_progression)

    def update(self):
        self.pos += self.vel

    def collide(self):
        self.vel.reflect(Vector((0,-1)))


class Vortex(Entity):  # the goal of the level. Player collision with it will cause the level to increment.
    def __init__(self, x, y, width=64):
        self.x = x
        self.y = y
        self.pos = Vector((x, y))
        self.relative_pos = self.pos.copy()
        self.internal_clock = Clock()
        self.sprite = Sprite_Sheet([0,6])
        self.width = width
        self.radius = width/2

    def draw(self, canvas):
        self.internal_clock.increment_clock()
        if self.internal_clock.return_mod(3):
            if self.sprite.frame_index == [6,6]:
                self.sprite.set_frame([0,6])
            else: self.sprite.step_frame()
        self.sprite.draw(canvas, self.relative_pos, (self.width, self.width))



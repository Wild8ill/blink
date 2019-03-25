try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import *
from sprite import *
from util import *
from platforms import *
from sprite_sheet import *


#############################################################################################
# Player
class Entity:  # base class that encompasses players and enemies
    def collide(self, platform, direction, collision_coord):
        pass

    def entity_collisions(self, object):
        pass


class PlayerHeart:
    def __init__(self, numerical_value,
                 heart_value):  # hearts have set width and are rendered in the top left corner. all we need is an offset
        self.dimensions = 32
        self.x = 16 + numerical_value * 32
        self.pos = Vector((self.x, 20))
        if heart_value == "half":
            self.sprite = Sprite_Sheet([1, 5])
        else:
            self.sprite = Sprite_Sheet([2, 5])

    def draw(self, canvas):
        self.sprite.draw(canvas, self.pos, (self.dimensions, self.dimensions))


class Player(Entity):  # model the character as a ball for now convenient hitboxes
    def __init__(self, pos=Vector((0, 0)), vel=Vector((0, 0)), radius=32, columns=1, row=1, width=0, height=0,
                 map=None):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.diameter = radius * 2
        self.border = 1
        self.sprite = Sprite_Sheet([0, 3])
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
        self.relative_pos = Vector((width / 2, height / 2))

        self.direction = "right"

        self.lives = 3  # amount of lives
        self.heart_array = []
        self.update_hearts()

        self.clock = Clock()
        self.fall = True  # whether or not to fall due to gravity
        self.jumps = 2
        self.blink = 5

    # def offsetB(self):
    #     return self.pos.y + self.radius

    def update(self):
        if self.lives <= 0:
            return "Game Over"

        if self.level_finished:
            return "Next Level"

        self.pos.add(self.vel)

        # Removing X Velocity over time
        # Removes 1/2 each loop
        # When at less than 0.1 set to 0
        # if (self.vel.x > 0):
        #     if(self.vel.x < 0.1):
        #         self.vel.subtract(Vector((self.vel.x, 0)))
        #     else:
        #         tmpx = self.vel.x / 2
        #         self.vel.subtract(Vector((tmpx, 0)))

        # JOsh code - Wrong

        self.vel.x *= 0.9
        if math.fabs(self.vel.x) < 0.5:
            self.vel.x = 0

        # Adds some "Gravity"
        if self.fall:
            self.vel.subtract(Vector((0, -0.0981)))

        self.MAP.update_positions()  # calculates all relative positions for objects, now that player is set up properly

        # State Checking
        # What Sprite do we show
        if self.state == "rest":
            if self.direction == "right":
                self.sprite.set_frame([0, 3])
            else:
                self.sprite.set_frame([4, 2])

            for move in self.move_buffer:
                self.handle_move(move)

        elif self.state == "attack":
            if self.animation_frame == 0:
                if self.direction == "right":
                    self.sprite.set_frame([0, 0])
                else:
                    self.sprite.set_frame([8, 1])

            if self.clock.return_mod(4):
                if self.direction == "right":
                    self.sprite.step_frame()
                    self.move_right(4)
                else:
                    self.sprite.dec_frame()
                    self.move_left(4)
                self.animation_frame += 1

            if self.animation_frame == 8:
                self.animation_frame = 0
                self.state = "rest"
                self.remove_move("a")

        elif self.state == "blink" and not self.blink == 0:
            initial_pos = self.pos.copy()
            self.fall = False
            self.vel = Vector((0, 0))
            if self.clock.return_mod(4):
                if self.direction == "right":
                    self.sprite.step_frame()
                else:
                    self.sprite.dec_frame()
                self.animation_frame += 1

            if self.animation_frame == 5:
                self.animation_frame = 0
                self.state = "rest"
                self.remove_move("s")
                if self.direction == "right":
                    self.pos = initial_pos + Vector((160, 0))  # teleport as many blocks across
                else:
                    self.pos = initial_pos + Vector((-160, 0))  # teleport as many blocks across
                self.fall = True
                self.blink -= 1

        self.vector_transform = Vector((self.WIDTH / 2, self.HEIGHT / 2)) - (self.pos)
        self.clock.increment_clock()

    def draw(self, canvas):
        # canvas.draw_circle((self.WIDTH / 2, self.HEIGHT / 2),
        #                    self.radius,
        #                    1,
        #                    "blue",
        #                    "blue")
        self.sprite.draw(canvas, Vector((self.WIDTH / 2, self.HEIGHT / 2)), (self.diameter, self.diameter))
        for heart in self.heart_array:
            heart.draw(canvas)

    ##################################################################
    # Player Move Handling

    def add_move(self, key):
        self.move_buffer.append(key)

    def remove_move(self, key):
        for key in self.move_buffer:
            self.move_buffer.remove(key)

    def handle_move(self, move):
        if move == simplegui.KEY_MAP["up"]:
            if self.jumps != 0:
                self.jump()
            self.remove_move(move)
        if move == simplegui.KEY_MAP["left"]:
            self.move_left(3)
        if move == simplegui.KEY_MAP["right"]:
            self.move_right(3)
        if move == simplegui.KEY_MAP["a"]:
            self.__setstate__("attack")
        if move == simplegui.KEY_MAP["s"]:
            self.__setstate__("blink")

    def move_left(self, speed):
        self.direction = "left"
        if math.fabs(self.vel.x) < self.terminal_vel:
            self.vel.add(Vector((-speed, 0)))

    def move_right(self, speed):
        self.direction = "right"
        if math.fabs(self.vel.x) < self.terminal_vel:
            self.vel.add(Vector((speed, 0)))

    def jump(self):
        self.vel.y = 0
        self.vel.add(Vector((0, -3)))
        self.jumps -= 1

    def __setstate__(self, state):
        self.state = state

    def collide(self, platform, direction, collision_coord):
        # self.vel.reflect(Vector((0,-1)))
        if isinstance(platform, SpikeBlock):
            self.take_hit(1)

        # assume block
        if direction == "left":
            self.pos.x = collision_coord - self.radius
            self.vel.x = 0
        if direction == "right":
            self.pos.x = collision_coord + self.radius
            self.vel.x = 0
        if direction == "top":
            self.pos.y = collision_coord - self.radius
            self.vel.y = 0
            self.jumps = 2
        if direction == "bottom":
            self.pos.y = collision_coord + self.radius
            self.vel.y = 0

    def entity_collisions(self, object):
        if isinstance(object, Vortex):
            self.level_finished = True
        if isinstance(object, Blip):
            self.take_hit(0.5)
        if isinstance(object, Bibble):
            self.vel.x = self.terminal_vel
            self.vel.reflect(Vector((-1,-1)))

    def update_hearts(self):
        self.heart_array = []
        for full_heart in range(0, math.floor(self.lives)):
            self.heart_array.append(PlayerHeart(full_heart, "full"))
        if self.lives % 1 != 0:
            self.heart_array.append(PlayerHeart(math.floor(self.lives), "half"))

    def take_hit(self, damage):
        self.lives -= damage
        self.update_hearts()


#################################################
# ENEMY

class Enemy(Entity):
    def __init__(self, x, y, frame_index = [0,0], radius=16):
        self.x = x
        self.y = y
        self.radius = radius
        self.pos = Vector((x, y))
        self.relative_pos = self.pos
        self.sprite = Sprite_Sheet(frame_index)

    def draw(self, canvas):
        self.sprite.draw(canvas, self.relative_pos, (self.radius * 2, self.radius * 2))


class Blip(Enemy):
    def __init__(self, x, y, velocity):
        self.vel = Vector((0, velocity))
        super().__init__(x, y, [0, 4])

    def update(self):
        self.pos += self.vel

    def collide(self, platform, direction, collision_coord):
        self.vel.reflect(Vector((0, -1)))

class Bibble(Enemy):
    def __init__(self, x, y, velocity):
        self.vel = Vector((velocity, 0))
        super().__init__(x, y, [4,4])
        self.internal_clock = Clock()
        self.flip_flop = 2 # allows frame to go up and down


    def update(self):
        self.internal_clock.increment_clock()
        self.pos += self.vel
        if self.internal_clock.return_mod(5):
            if self.flip_flop == 2 or self.flip_flop == 4:
                self.flip_flop += 1
            else:
                self.flip_flop -= 1
            self.sprite.set_frame([self.flip_flop,4])

        if self.internal_clock.return_mod(48): # every 2 blocks or so
            self.vel.reflect(Vector((-1,0)))
            if self.flip_flop == 2 or self.flip_flop == 3:
                self.flip_flop = 4
            else:
                self.flip_flop = 2

    def collide(self, platform, direction, collision_coord):
        self.vel.reflect(Vector((0, -1)))


class Vortex(Entity):  # the goal of the level. Player collision with it will cause the level to increment.
    def __init__(self, x, y, width=64):
        self.x = x
        self.y = y
        self.pos = Vector((x, y))
        self.relative_pos = self.pos.copy()
        self.internal_clock = Clock()
        self.sprite = Sprite_Sheet([0, 6])
        self.width = width
        self.radius = width / 2

    def draw(self, canvas):
        self.internal_clock.increment_clock()
        if self.internal_clock.return_mod(3):
            if self.sprite.frame_index == [6, 6]:
                self.sprite.set_frame([0, 6])
            else:
                self.sprite.step_frame()
        self.sprite.draw(canvas, self.relative_pos, (self.width, self.width))

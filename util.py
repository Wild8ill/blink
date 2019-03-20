try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import *
from sprite import *
from abc import ABC, abstractmethod


class Camera:  # the object that returns the locations of all the objects to be drawn to the screen, and handles vector transformations
    def __init__(self, width, height, player, map):
        # constants
        self.WIDTH = width
        self.HEIGHT = height
        self.PLAYER = player
        self.X = 0
        self.Y = 1  # used to get values from the midpoint tuple
        self.MAP = map  # the map of all the objects in the level        self.move_state = "static"
        self.midpoint = self.PLAYER.pos.getP()
        self.background = [Background(Vector((self.WIDTH / 2, self.HEIGHT / 2)))]
        self.midground = [Midground(Vector((self.WIDTH / 2, self.HEIGHT / 2)))]
        self.foreground = [Foreground(Vector((self.WIDTH / 2, self.HEIGHT / 2)))]

        self.update()

    def update(self):  # update
        if (self.midpoint[self.X] < self.PLAYER.pos.getP()[self.X]):
            self.move_state = "right" # purely for readabillity, actually irrelevant
        elif (self.midpoint[self.X] > self.PLAYER.pos.getP()[self.X]):
            self.move_state = "left"
        else:
            self.move_state = "static"

        for tile in self.background:
            tile.scroll(self.move_state)

        for tile in self.midground:
            tile.scroll(self.move_state)

        for tile in self.foreground:
            tile.scroll(self.move_state)

        self.background_calculation(self.foreground)
        self.background_calculation(self.midground)
        self.background_calculation(self.background)



        self.midpoint = self.PLAYER.pos.getP()
        self.left_edge = self.midpoint[self.X] - self.WIDTH / 2
        self.right_edge = self.midpoint[self.X] + self.WIDTH / 2
        self.top_edge = self.midpoint[self.Y] - self.WIDTH / 2
        self.bottom_edge = self.midpoint[self.Y] + self.WIDTH / 2


    def background_calculation(self, list_of_tiles):
        main_tile = list_of_tiles[0] # always at least one
        if isinstance(main_tile, Background):
            copy_tile = Background(main_tile.pos.copy())
        elif isinstance(main_tile, Midground):
            copy_tile = Midground(main_tile.pos.copy())
        elif isinstance(main_tile, Foreground):
            copy_tile = Foreground(main_tile.pos.copy())

        if main_tile.left_edge >= 0 and not main_tile.left_neighbour:
            copy_tile.pos.x = 0-copy_tile.WIDTH/2
            main_tile.left_neighbour = True
            list_of_tiles.append(copy_tile)

        if main_tile.right_edge <= self.WIDTH and not main_tile.right_neighbour:
            copy_tile.pos.x = self.WIDTH + copy_tile.WIDTH / 2
            main_tile.right_neighbour = True
            list_of_tiles.append(copy_tile)

        if main_tile.right_edge <= 0 or main_tile.left_edge >= self.WIDTH:
            list_of_tiles.remove(main_tile)

    def objects_to_render(self):
        temp_objects = [tile for tile in self.background + self.midground + self.foreground] # don't ask for your sake
        temp_objects.append(self.PLAYER)

        for object in self.MAP:
            if self.within_bounds(object.pos.getP()):
                temp_objects.append(object)
        return temp_objects

    def within_bounds(self, position):
        x = position[self.X]
        y = position[self.Y]
        if x <= self.right_edge + 16 and x >= self.left_edge - 16:  # checks x coordinate against the edges. Added a tolerance for smoothness
            if y >= self.top_edge - 16 and y <= self.bottom_edge + 16:  # checks y, note y increases downwards
                return True
        return False

    def __str__(self):
        return str(self.midpoint)

class Clock:
    def __init__(self):
        self.__clock = 0

    def increment_clock(self):
        self.__clock += 1

    def return_mod(self, mod):
        if self.__clock % mod == 0:
            return True
        return False

    def __str__(self):
        return str(self.__clock)

class Line:  # a purely theoretical line class used to return the hitbox of platforms
    def __init__(self, pointA, pointB):
        self.pointA = pointA
        self.pointB = pointB
        self.thickness = 1
        self.unit = (self.pointB - self.pointA).normalize()
        self.normal = self.unit.copy().rotate_90()

    def draw(self, canvas):  # for error testing allow the line to be drawn
        canvas.draw_line(self.pointA.getP(), self.pointB.getP(), self.thickness, 'White')

    def distance_to_object(self, pos):  # distance from the point handed to the line. Maths covered in lectures
        vector_to_a = pos - self.pointA
        projection = vector_to_a.dot(self.normal) * self.normal
        return projection.length()

    def within_points(self, pos):  # ensures that the object is hitting within the confines of the line
        return ((pos - self.pointA).dot(self.unit) >= 0 and
                (pos - self.pointB).dot(-self.unit) >= 0)

class Parallax:
    def __init__(self, pos):
        self.pos = pos
        self.scroll_speed = 1
        self.WIDTH = 2000
        self.HEIGHT = 1000
        self.left_edge = self.pos.getP()[0] - self.WIDTH / 2
        self.right_edge = self.pos.getP()[0] + self.WIDTH / 2
        self.left_neighbour = False
        self.right_neighbour = False
        self.IMG = "https://i.postimg.cc/6qzLMjBr/parallax.png"
        self.sprite = Sprite(self.IMG, 1, 3)


    def draw(self, canvas):
        self.sprite.draw(canvas, self.pos, (self.WIDTH, self.HEIGHT), self.sprite.frame_index)


    def scroll(self, direction):
        if (direction == "left"):
            self.pos -= Vector((self.scroll_speed, 0))
        elif (direction == "right"):
            self.pos += Vector((self.scroll_speed, 0))
        self.left_edge = self.pos.getP()[0] - self.WIDTH / 2
        self.right_edge = self.pos.getP()[0] + self.WIDTH / 2


class Background(Parallax):
    def __init__(self, pos):
        super().__init__(pos)
        self.sprite.set_frame([0,0])

class Midground(Parallax):
    def __init__(self, pos):
        super().__init__(pos)
        self.scroll_speed /= 0.6
        self.sprite.set_frame([0,1])

class Foreground(Parallax):
    def __init__(self, pos):
        super().__init__(pos)
        self.scroll_speed /= 0.3
        self.sprite.set_frame([0,2])

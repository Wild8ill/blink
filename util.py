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
        self.MAP = map  # the map of all the objects in the level

        self.update()

    def update(self):  # update
        self.midpoint = self.PLAYER.pos.getP()
        self.left_edge = self.midpoint[self.X] - self.WIDTH / 2
        self.right_edge = self.midpoint[self.X] + self.WIDTH / 2
        self.top_edge = self.midpoint[self.Y] - self.WIDTH / 2
        self.bottom_edge = self.midpoint[self.Y] + self.WIDTH / 2

    def objects_to_render(self):
        temp_objects = [self.PLAYER]
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

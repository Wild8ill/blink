try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import *
from sprite import *
from map_constructor import *

WIDTH = 800
HEIGHT = 450
clock = 0
player = None  # will be overwritten
MAP_CONSTRUCTOR = MapConstructor(HEIGHT)
map = None

def return_level_file(level_id):
    level_dict = {
        1:"testmap.png",
        2:"level2.png"
    }
    return level_dict.get(level_id)


def setup_level(level_id):
    global MAP_CONSTRUCTOR, map, player
    map = MAP_CONSTRUCTOR.generate_map("levels/"+return_level_file(level_id)) # gets the map corresponding to the level id passed
    for object in map:
        if isinstance(object, Player):
            player = object

#############################################################################################
# Collision

## What is needed
### - 
### 
### 
class Interaction:
    def __init__(self):
        # Arr of Collision_Handler
        self.collisionArr = []



# Handles the collision between two objects
class Collision_Handler:
    def __init__(self, obj_1, obj_2):
        self.obj_1 = obj_1
        self.obj_2 = obj_2
        # State of collision
        self.isColliding = False

    # Will say collision is True when collision happens
    def collision_check(self):
        distance_vector = Vector((self.obj_2.pos)) - Vector((self.obj_1.pos))
        distance = distance_vector.length()
        if distance <= self.obj_1.radius + self.obj_2.radius:
            if not self.isColliding: 
                self.isColliding = True
        self.isColliding = False

    # Check the type of the objects colliding
        # Then perform an action based on the type of collison happening
    def collision_action(self):  
        # Check if Player
        if isinstance(self.obj_1,  Player): # Check if instance of Player
            if isinstance(self.obj_2, Enemy):
                pass
            if isinstance(self.obj_2, Platform):
                pass

        # Check if Platform      
        if isinstance(self.obj_1, Platform): # Check if instance of Platform
            if isinstance(self.obj_2, Player): # Check if instance of Player
                pass
            if isinstance(self.obj_2, Enemy): # Check if instance of AI
                pass

        # Check if AI
        if isinstance(self.obj_1,  Enemy): # Check if instance of AI
            if isinstance(self.obj_2, Player):
                pass
            if isinstance(self.obj_2, Platform):
                pass


#############################################################################################
# Game Logic

###############
# Handlers
def draw_handler(canvas):
    global WIDTH, HEIGHT, sprite, map, player
    for object in map:
        object.draw(canvas)
    #player.draw(canvas)
    player.sprite.step_frame()

def key_down_handler(key):
    player.add_move(key)

def key_up_handler(key):
    player.remove_move(key)

def timer_handler():
    global clock
    clock += 1

###############
# Rest of Code
setup_level(2)
timer = simplegui.create_timer(1, timer_handler)
timer.start()

frame = simplegui.create_frame('Testing', WIDTH, HEIGHT)
frame.set_draw_handler(draw_handler)
frame.set_keydown_handler(key_down_handler)
frame.set_keyup_handler(key_up_handler)
frame.start()

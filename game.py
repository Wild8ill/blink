try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import *
from sprite import *
from map_constructor import *

WIDTH = 800
HEIGHT = 450
MAP_CONSTRUCTOR = MapConstructor(WIDTH,HEIGHT)
map = None
clock = Clock()

def return_level_file(level_id): # a dictionary wrapper to allow the generation and passing of levels automatically
    level_dict = {
        0:"welcome.png",
        1:"testmap.png",
        2:"level2.png",
        3:"level3.png",
        4:"level4.png"
    }
    return "levels/%s"%level_dict.get(level_id)


#############################################################################################
# Collision
# @ TODO: REDO ALL OF INTERACTION AND COLLISION AND MAKE IT WORK
class Interaction:
    def __init__(self):
        # Arr of Collision_Handler
        self.collisionArr = []
        #dictionary coantining key value pairs and collision handlers

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

    # actually ignore this. Pass through to the individual class for actions
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
class Game: 
    def __init__(self):
        # PLAYER LIFE
        self.MAXLIVES = 3
        self.currentLives = self.MAXLIVES
        # SCORE
        self.score = 0
        # In PLAY 
        self.inPlay = False # Are we playing the game or at main menu
        self.level = 4 # The Current Level
        # GAME ITEMS
        self.player = None  # will be overwritten
        self.camera = None # will also be overwritten

    # Handles the drawing of the game
    def draw(self, canvas):
        # Only draw objects that are in the cameras view
        for object in self.camera.objects_to_render():
            if not isinstance(object, Player):
                object.draw(canvas)

        # Update the current level
        if self.player.update(clock) == "Next Level":
            self.level += 1 # Increase the level id of the game object
            self.setup_level() # Call the constructor of the object
        
        # Draw the player
        self.player.draw(canvas)
        MAP_CONSTRUCTOR.PLAYER = self.player # make player current so vector transform is updated
        self.camera.update()

    # Update the current level then run the setup for it
        ## Added so we can force level skipping to test
    def set_level(self, level):
        self.level = level
        self.setup_level()

    # Construct the current level
    def setup_level(self):
        global MAP_CONSTRUCTOR, map
        map = MAP_CONSTRUCTOR.generate_map(return_level_file(self.level)) # gets the map corresponding to the level of the game object.
        for object in map:
            if isinstance(object, Player):
                self.player = object
                self.camera = Camera(WIDTH,HEIGHT, self.player, map)


###############
# Event Handling
class Events:
    def __init__(self):
        pass

    def key_down(self, key):
        game.player.add_move(key)

    def key_up(self, key):
        game.player.remove_move(key)

    def timer(self):
        global clock
        clock.increment_clock()

###############
# Rest of Code

# Initialisation of Game
game = Game()
game.setup_level()

# Canvas and Drawing Setup
frame = simplegui.create_frame('Blink', WIDTH, HEIGHT)
frame.set_draw_handler(game.draw)

# Event Handling
event = Events() # Event Handler Object
timer = simplegui.create_timer(1, event.timer)
    # Register Key down and Key Up events of key press
frame.set_keydown_handler(event.key_down) # On Key Down
frame.set_keyup_handler(event.key_up) # On Key Up

# Event Handling
timer.start()
frame.start()

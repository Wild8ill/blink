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
        3:"level3.png"
    }
    return level_dict.get(level_id)


#############################################################################################
# Collision
# @ TODO: REDO ALL OF INTERACTION AND COLLISION AND MAKE IT WORK
class Interaction:
    def __init__(self):
        # Arrays of objects
        self.collisionArr = []

    def addCollidable(self, obj1, obj2):
        self.collisionArr.append(Collidable(obj1, obj2))

    def update(self):
        for collidable in self.collisionArr:
            collidable.update()

# Handles the collision between two objects
class Collidable:
    def __init__(self, obj_1, obj_2):
        self.obj_1 = obj_1
        self.obj_2 = obj_2
        # State of collision
        self.isColliding = False

    # Will say collision is True when collision happens
        # From there you can apply logic of what to do in response
    def update(self):
        # @TODO: Create logic for comparing objects to check collision that works
        pass
        # distance_vector = Vector((self.obj_2.pos)) - Vector((self.obj_1.pos))
        # distance = distance_vector.length()
        # if distance <= self.obj_1.radius + self.obj_2.radius:
        #     if not self.isColliding:
        #         self.isColliding = True
        # self.isColliding = False

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
        self.level = 1 # The Current Level
        # GAME ITEMS
        self.player = None  # will be overwritten
        self.camera = None # will also be overwritten
        # Interactions
        self.interaction = Interaction() # The Interactions (Collisions)
        # Game Objects
        self.platformArr = []
        self.entityArr = []

        
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
        self.update() # Update Game Logic


    # What to do every update
    def update(self):
        self.interaction.update() # Check every interaction
        self.camera.update()

    # On new map run this to get every interaction to be modelled
        # Added to the interaction object as a collidable
    def model_interactions(self):
        for entity in self.entityArr:
            for platform in self.platformArr:
                self.interaction.addCollidable(entity, platform)

    # Update the current level then run the setup for it
        ## Added so we can force level skipping to test
    def set_level(self, level):
        self.level = level
        self.setup_level()

    # Construct the current level
    def setup_level(self):
        global MAP_CONSTRUCTOR, map
        map = MAP_CONSTRUCTOR.generate_map("levels/"+return_level_file(self.level)) # gets the map corresponding to the level of the game object.
        for object in map:
            if isinstance(object, Player):
                self.player = object
                self.camera = Camera(WIDTH,HEIGHT, self.player, map)
                self.entityArr.insert(0, object) # Adds player to the first position of the Entity Array
            elif isinstance(object, Enemy):
                self.entityArr.append(object) # Adds Enemies to the Entity Array
            else:
                self.platformArr.append(object) # Adds platforms to Platform Array
        self.model_interactions() # Models the interactions between every Platform and Entity


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

# Event Handlong
event = Events() # Event Handler Object
timer = simplegui.create_timer(1, event.timer)
    # Register Key down and Key Up events of key press
frame.set_keydown_handler(event.key_down) # On Key Down
frame.set_keyup_handler(event.key_up) # On Key Up

print("big yeet")
# Event Handling
timer.start()
frame.start()

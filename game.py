try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import *
from sprite import *
from map_constructor import *
from platforms import *
from entity import *
from util import *

WIDTH = 800
HEIGHT = 450
MAP_CONSTRUCTOR = MapConstructor(WIDTH,HEIGHT)
map = None
#clock = Clock()

def return_level_file(level_id): # a dictionary wrapper to allow the generation and passing of levels automatically
    level_dict = {
        -1:"gameover.png",
        0:"welcome.png",
        1:"testmap.png",
        2:"level2.png",
        3:"level3.png",
        4:"level4.png",
        5:"level5.png",
        6: "collision_test.png"
    }
    return "levels/%s"%level_dict.get(level_id)


#############################################################################################
# Collision
class Interaction:
    def __init__(self):
        # Arrays of objects
        self.platformCollisionArr = [] # Every Entity V Platform
        self.entityCollisionArr = []  # Player V Entity

    # Collision of Entity vs Platform/Object
    def addPlatformCollidable(self, entity, obj2):
        self.platformCollisionArr.append(PlatformCollidable(entity, obj2))

    # Collision of Entity vs Entity
    def addEntityCollidable(self, entity_one, entity_two):
        self.entityCollisionArr.append(EntityCollidable(entity_one, entity_two))

    def update(self):
        # Update all entity vs platform collisions
        for platformCollidable in self.platformCollisionArr:
            platformCollidable.update()
        # Update all entity vs entity collisions
        for entityCollidable in self.entityCollisionArr:
            entityCollidable.update()


# Handles the collision between two objects
class Collidable:
    def __init__(self, obj_1, obj_2):
        self.obj_1 = obj_1
        self.obj_2 = obj_2
        # State of collision
        self.isColliding = False

class PlatformCollidable(Collidable):    
    # Obj 1 = Entity = Sphere
    # Obj 2 = Platform = Rectangle 
    def update(self):
        # @TODO: Create logic for comparing objects to check collision that works
        object = self.obj_1
        platform = self.obj_2
        line_tuple = platform.return_hitbox()
        for line in line_tuple:
            if line.distance_to_object(object.relative_pos) < object.radius and line.within_points(object.relative_pos):
                if not self.isColliding:
                    if line == line_tuple[0]:
                        direction = "left"
                        collision_coord = platform.pos.copy().x - platform.block_width/2
                    if line == line_tuple[1]:
                        direction = "top"
                        collision_coord = platform.pos.copy().y - platform.block_width/2
                    if line == line_tuple[2]:
                        direction = "right"
                        collision_coord = platform.pos.copy().x + platform.block_width/2
                    if line == line_tuple[3]:
                        direction = "bottom"
                        collision_coord = platform.pos.copy().y + platform.block_width/2


                    #object.vel = Vector((0,0))
                    object.collide(platform, direction, collision_coord)
                     # TODO: ADD LOGIC FOR WHAT TO DO ON COLLISION
                    self.isColliding = True
            else:
                self.isColliding = False

class EntityCollidable(Collidable):  
    # Obj 1 = Entity = Sphere
    # Obj 2 = Entity = Sphere
    def update(self):
        # @TODO: Create logic for comparing objects to check collision that works
        distance_vector = Vector((self.obj_2.relative_pos.getP())) - Vector((self.obj_1.relative_pos.getP()))
        distance = distance_vector.length()
        if distance <= self.obj_1.radius + self.obj_2.radius:
            if not self.isColliding:
                self.obj_1.entity_collisions(self.obj_2)
                self.obj_2.entity_collisions(self.obj_1)
                self.isColliding = True
        else:
            self.isColliding = False

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
        self.level = 0# The Current Level
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

        draw_above_player = [] # for exceptional things to be drawn over player

        for object in self.camera.objects_to_render():
            if isinstance(object, StaticScreen):
                draw_above_player.append(object)
                break
        draw_over_player = [] #used for static screens
        for object in self.camera.objects_to_render():

            if isinstance(object, StaticScreen):
                draw_over_player.append(object)
                break

            if not isinstance(object, Player):
                object.draw(canvas)
                if isinstance(object,Enemy):
                    object.update()

        # Update the current level
        #if self.player.update(clock) == "Next Level":
        if self.player.update() == "Next Level":
            self.level += 1 # Increase the level id of the game object
            self.setup_level() # Call the constructor of the object

        if self.player.update() == "Game Over":
            self.level = -1
            self.setup_level() # Call the constructor of the object

        
        # Draw the player
        self.player.draw(canvas)

        for object in draw_above_player:
            object.draw(canvas)

        MAP_CONSTRUCTOR.PLAYER = self.player # make player current so vector transform is updated
        self.update() # Update Game Logic


    # What to do every update
    def update(self):
        self.interaction.update() # Check every interaction
        self.camera.update()

    # On new map run this to get every interaction to be modelled
        # Added to the interaction object as a collidable
    def model_interactions(self):
        # Every Entity vs Platform Interaction
        for entity in self.entityArr:
            for platform in self.platformArr:
                self.interaction.addPlatformCollidable(entity, platform)
        # Every Entity vs Entity
        for entityOne in self.entityArr:
            for entityTwo in self.entityArr:
                if entityOne is not entityTwo:
                    self.interaction.addEntityCollidable(entityOne, entityTwo)

    # Update the current level then run the setup for it
        ## Added so we can force level skipping to test
    def set_level(self, level): 
        self.level = level
        self.setup_level()

    # Construct the current level
    def setup_level(self):
        self.platformArr = []
        self.entityArr = []
        global MAP_CONSTRUCTOR, map
        map = MAP_CONSTRUCTOR.generate_map(return_level_file(self.level)) # gets the map corresponding to the level of the game object.
        
        # Create camera object
        # Go through items of map until find the player object
        for object in map:
            if isinstance(object, Player):
                self.player = object
                self.camera = Camera(WIDTH,HEIGHT, self.player, map)
                self.entityArr.insert(0, object) # Adds player to the first position of the Entity Array

        # Go through all objects rendered by the camera
        # for object in self.camera.objects_to_render():
        for object in map:
            if isinstance(object, Entity) and not isinstance(object,Player):

                self.entityArr.append(object) # Adds Enemies to the Entity Array
            elif isinstance(object,Platform):
                self.platformArr.append(object) # Adds platforms to Platform Array
            else:
                pass
        self.model_interactions() # Models the interactions between every Platform and Entity


###############
# Event Handling
class Events:
    def __init__(self):
        pass

    def key_down(self, key):
        game.player.add_move(key)

    def key_up(self, key):
        if key == simplegui.KEY_MAP["space"] and (game.level == -1 or game.level == 0):
            game.level += 1
            game.setup_level()

        game.player.remove_move(key)

    # def timer(self):
    #     global clock
    #     clock.increment_clock()

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
#timer = simplegui.create_timer(1, event.timer)
    # Register Key down and Key Up events of key press
frame.set_keydown_handler(event.key_down) # On Key Down
frame.set_keyup_handler(event.key_up) # On Key Up

# Event Handling
#timer.start()
frame.start()

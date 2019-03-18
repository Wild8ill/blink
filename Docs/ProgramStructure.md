# Program Structure
## Table of Contents
- [Program Structure](#program-structure)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Game.py](#gamepy)
    - [Game Logic](#game-logic)
    - [Interactions](#interactions)
    - [Events](#events)
  - [Platforms.py](#platformspy)
    - [Platform](#platform)
  - [Entity.py](#entitypy)
    - [Entity](#entity)
    - [Player](#player)
    - [Enemy](#enemy)
    - [Blip(Enemy)](#blipenemy)
  - [Util.py](#utilpy)
    - [Camera](#camera)
    - [Clock](#clock)
    - [Line](#line)


## Introduction
The main files we use in our project are:
    - game.py
    - platforms.py
    - entity.py
    - util.py
    - sprite.py
    - vector.py
    - map_constructor.py

In this document I will be going over what these files contain and how they interact.

- Platform
  - FloatingPlatform

- Camera
- Line


## Game.py
`game.py` is the entrypoint into our game.
Inside of which we have the following classes:
    - Interaction
    - Collidable
    - PlatformCollidable(Collidable)
    - EntityCollidable(Collidable)
    - Game
    - Events

At the top of the file we:
    - Import required dependencies
    - Set WIDTH and HEIGHT
    - Create and intance of the `MAP_CONSTRUCTOR`
    - Define the map variable.
    - Create a clock obejct.
    - We also define `return_level_file` which is a function that maps a level_id to the respective level.


At the bottom of the file we:
  - Initialise the `Game` object.
  - Run `game.setup_level` to load the level
  - Create a frame, and set the draw handler to be the `draw` call of the `game` object.
  - Initalise the `Event` object
  - Map simplegui events to relate to our respective methods of the `event` object.
  - start the timer.
  - start the frame

### Game Logic
All of our game logic is handled inside of the `Game` class.
Inside of which we have the following variables:

  - `MAXLIVES`: The max number of lives a player is able to have
  - `CurrentLives`: The current number of lives a player has (Default = MAXLIVES)
  - `Score`: The current score of the player (Default 0)
  - `inPlay`: Whether we are in the game or at menu. (Default false: For menu)
  - `level`: The level the player is currently at (Default 1)
  - `player`: Reference to the `Player` object
  - `camera`: Reference to the `Camera` object
  - `interaction`: Instance of `Interaction` class. Handles our interactions + Collisions.
  - `platformArr`: Array of all `Platform` objects in the level
  - `entityArr`: Array of all `Player` and `Enemey` objects in the level
    - `Player` should be stored at position [0]

The class has the following **methods**:
  - `draw()`: The main draw handler for our game.
    - Draws all objects that are currently in the cameras view
    - Updates the level when needed
    - Draws the player
    - Calls *self.update* to update game logic
  - `update()`: Logic updating method
    - Every *tick*, this is called and logic is updated
    - e.g. the update call of classes are called such as `interaction.update()`
  - `model_interaction`: When a new map is loaded this initialises the Collidable objects for the map. Stored with the interaction object.
  - `set_level`: Allows us to force the level to be changed to the given ID.
  - `setup_level`: Construct the level, use the `MAP_CONSTRUCTOR` class to generate the map from the given level image.
    - Store all objects. Platform, Entity into their given arrays.
    - If the object is the Player, insert to the start of the Entity Array
    - Call `model_interaction` to model all possible interactions.
  

### Interactions
We handle all of our interactions using the `Interaction` class, we instantiate this in our `Game` class. 
- Interaction contains two arrays.
  - One array of `platformCollisionArr` which contains all `Collidable` type objects between every entity and every platform.
  - One array of `entityCollisionArr` which contains all `Collidable` type objects between every entity and every *other* entity.
- We have two methods to create a new instance of a `Collidable`
  - `addPlatformCollidable`. This models a relation between an entity and a platform
  - `addEntityCollidable`. This models a relation between an entity and another entity.
  
Our relations for collisions are stored as an instance of `Collidable` (To more specifc subclasses of Collidable)
- These contain three variables,
  - obj1 : The first object
  - obj2 : The second object
  - isColliding: Are these objects current colliding?

The reason we have two types of `Collidable` is inside of each of these types `PlatformCollidable` and `EntityCollidable` we have seperate update calls which check the collision between the two given objects.

Every time the `update` method is called on the interaction object. Each `Collidable` has its own respective update call ran on itself.

### Events
This class is to handle any events the game has. This is a class just so we have a dedication section to control events.
- `key_down`: When any key is pressed down add the move to the player.
- `key_up`: When any keypress is removed remove the move from the player.
- `timer`: Handles the incremting of the clock.


## Platforms.py
`platforms.py` is the file in which we store the definition of the platforms.

### Platform
The platform Class is the template for one of the ingame platforms, which are square blocks.
It has the following variables:
  - y: The y value of the platform
  - x: The x value of the platform
  - color: The color of the platform
  - sprite: The sprite of the platform (The image to be displayed)
  - pos: The position of the platform( Vector of (x,y))
  - relative_pos: The relative position to the *camera*
  - block_width: The width of the block

It has the folllowing functions:
  - draw(): Draws the sprite to the screen in its given position
  - return_hitbox(): Returns 4 lines defining the outer edges of the block
  

## Entity.py
`entity.py` is the file where we store the definitions for all entities. Such as:
- Entity
  - Player
  - Enemy
    - Blip

### Entity
The superclass of all "Entities". All it does is group them together.

### Player
The `Player` class is a subclass of `Entity`.
  - The hitbox is circular
  - It has different "States" which control its sprite
  
It contains the following variables:
- `pos`: The current position. It is a Vector.
- `Vel`: The current velocity of the Player. It is a Vector.
- `Radius`: The radius of the hitbox of the player.
- `Diameter`: The radius * 2
- `Border`: The size of the border of the circle
- `Sprite`: The instantiated `Sprite` class for the player.
- `move_buffer`: Moves are added to this buffer when a key event is handled. When an update cycle is ran a move is removed.
- `collision`: Array of items the Player is colliding with
- `state`: The current state fo the player, relates to the sprite shown.
- `animation_frame`: The current frame being shown
- `WDITH`: The width of the player
- `HEIGHT`: The height of the player
- `MAP`: The current map
- `vector_transform`: ??
- `level_finished`: Is the level complete
- `relative_pos`: The players position relative to the camera/canvas


The methods is has are:
- `update`: 
  - ?? Level Checking ?? **Move this out into Game?**
  - State Checking. Check what state it is and update frame and move_buffer accordingly
- `draw`: Draw the spirte onscreen
- `add_move`: Add the given move to the `move_buffer` array
- `remove_move`: Remove the given move from the `move_buffer` array
- `handle_move`: Handle the given action, e.g. Set State
- `move_left`: Move the player left
- `move_right`: Move the player right
- `jump`: Make the player jump
- `__setstate__`: Set the state of the player
- `collide`: Set the velocity to 0
- `check_collision`: If the collision array has something in it, check if it is platform and check.


### Enemy
The `Player` class is a subclass of `Entity`.
  - The hitbox is circular

It contains the follow variables:
- `x`: The x Position
- `y`: The y Position
- `radius`: The radius of the hitbox
- `pos`: The position, Vector of (x,y)
- `relative_pos`: The position relative to the camera/canvas
- `sprite_progression`: The current position in its sprite
- `sprite`: Instance of `Sprite` for the enemy. 

It contains the following methods:
- `draw()`: Draws the enemy on screen

### Blip(Enemy)
Blip is a subclass of Enemy, it is a type of enemy in the game.

It contains the following extra variables:
- `vel`: The velocity of the object
- `sprite_progression`: Its progression through the spritesheet

It contains the following methods:
- `update`: Updates the logic of the object
  - Adds the velocity to the position, otherwise known as moving it
- `collide`: Reflects the object on its current velocity.

## Util.py

### Camera
This object returns the locations of all objects to be drawn on the screen along with handling vector transformations.

It has the following variables:
- `WIDTH`: The width of the view
- `HEIGHT`: The height fo the view
- `PLAYER`: Reference to the player object.
- `X`
- `Y`
- `MAP`: The map of all objects found within the level

It contains the following methods
- `update()`: Moves the camera every call
- `objects_to_render()`: Returns an array of all objects that should be rendered in the current scene.
- `within_bounds`: Checks if the camera is within bounds

### Clock
A simple object that tracks the number of iterations.

### Line
A class used to generate lines between given points. It is used with Platforms and their collisions. 
- It allows us to generate 4 lines depicting the edges of the platform.

It contains the following variables:
- `pointA`: The first point
- `pointB`: The second point
- `thickness`: The thickness of the given line
- `unit`: The unit vector
- `normal`: The normal of the line

It contains the following methods:
- `draw`: Draws the line on screen. Used for error testing
- `distance_to_object`: Calculates the distance from the given position to the line.
- `within_points`: Checks to see if the object colliding is in the lines.


# Program Structure
The main files we use in our project are:
    - game.py
    - objects.py
    - sprite.py
    - vector.py
    - map_constructor.py

In this document I will be going over what these files contain and how they interact.


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
    - MAXLIVES: The max number of lives a player is able to have
    - CurrentLives: The current number of lives a player has (Default = MAXLIVES)
    - Score: The current score of the player (Default 0)
    - inPlay: Whether we are in the game or at menu. (Default false: For menu)
    - level: The level the player is currently at (Default 1)
    - player: Reference to the `Player` object
    - camera: Reference to the `Camera` object
    - interaction: Instance of `Interaction` class. Handles our interactions + Collisions.
    - platformArr: Array of all `Platform` objects in the level
    - entityArr: Array of all `Player` and `Enemey` objects in the level
      - Player should be stored at position [0]

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


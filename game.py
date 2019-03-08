try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import *
from sprite import *

#IMG = 'http://www.cs.rhul.ac.uk/courses/CS1830/sprites/runnerSheet.png'
#IMG = 'https://i.postimg.cc/vH7ssn2z/piggie.png'
#IMG = 'https://i.postimg.cc/bwkbkgb4/excalibur.png'
IMG ='https://i.postimg.cc/gJr7sJWX/attack.png'
sprite = Sprite(IMG, 9, 1)
WIDTH = 500
HEIGHT = 500
count = 0
clock = 0

#############################################################################################
# Platform
class Platform:
    def __init__(self, y, border, color):
        self.y = y
        self.border = border
        self.color = color
        self.normal = Vector((0, 1))
        self.edgeR = y + 1 + self.border

    def draw(self, canvas):
        canvas.draw_line((0, self.y),
                         (WIDTH, self.y),
                         self.border * 2 + 1,
                         self.color)

    def hit(self, obj):
        h = (obj.offsetB() >= self.edgeR)
        return h

#############################################################################################
# Player
# @TODO: If Left Flip Sprite
class Player: # model the character as a ball for now convenient hitboxes
    def __init__(self, pos, vel, radius, image, columns,row):
        self.dir = "right"
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.diameter = radius*2
        self.border = 1
        self.sprite = Sprite(image,columns,row)
        self.move_buffer = []
        self.collision = []
        self.state = "rest"
        self.animation_frame = 0

    def offsetB(self):
        return self.pos.y + self.radius

    def update(self):
        global clock
        self.pos.add(self.vel)
        self.vel.subtract(Vector((0,-0.0981)))
        if self.state == "rest":
            sprite.set_frame([8,0])
            for move in self.move_buffer:
                self.handle_move(move)

        elif self.state == "attack":
            sprite.frame_index = [0,0]
            if clock % 3 == 0:
                sprite.step_frame()
                self.animation_frame += 1
            self.move_right(1)
            if self.animation_frame == 9:
                self.animation_frame = 0
                self.state = "rest"
                self.remove_move("a")

        elif self.state == "blink":
            if clock % 10 == 0:
                sprite.step_frame()
                self.animation_frame += 1
            if self.animation_frame == 9:
                self.animation_frame = 0
                self.state = "rest"
                self.remove_move("s")

        self.check_collision()


    def draw(self, canvas):
        '''canvas.draw_circle(self.pos.getP(),
                           self.radius,
                           1,
                           self.color,
                           self.color)
        '''
        sprite.draw(canvas, (self.pos), (self.diameter, self.diameter))

    def add_move(self,key):
        self.move_buffer.append(key)

    def remove_move(self,key):
        for key in self.move_buffer:
            self.move_buffer.remove(key)

    def handle_move(self,move):
        if move == simplegui.KEY_MAP["left"]:
            self.dir = "left"
            self.move_left(3)
        if move == simplegui.KEY_MAP["right"]:
            self.dir = "right"
            self.move_right(3)
        if move == simplegui.KEY_MAP["a"]:
            self.__setstate__("attack")
        if move == simplegui.KEY_MAP["s"]:
            self.__setstate__("blink")

    def move_left(self,speed):
        self.pos.add(Vector((-speed,0)))

    def move_right(self,speed):
        self.pos.add(Vector((speed,0)))

    def __setstate__(self, state):
        self.state = state

    def collide(self, object):
        self.collision.append(object)

    def check_collision(self):
        if len(self.collision) != 0:
            for object in self.collision:
                if isinstance(object,Platform):
                    self.vel.y = 0
                    self.pos.y = object.y - self.radius

#############################################################################################
# Interaction

class Interaction: # takes list of objects on screen and the player
    # Obj 1 = Item that hits another (ball)
    # Obj 2 = Item that gets "hit" (wall)
    def __init__(self, obj1, obj2):
        self.obj2 = obj2
        self.obj1 = obj1

    def update(self):
        if self.obj1.hit(self.obj2):
            self.obj2.collide(self.obj1)
        self.obj2.update()
        #print(self.wall.hit(self.ball))

    def draw(self, canvas):
        self.update()
        self.obj1.draw(canvas)
        self.obj2.draw(canvas)

#############################################################################################
# Collision

class Collision:
    def __init__(self,obj_1, obj_2):
        self.obj_1 = obj_1
        self.obj_2 = obj_2

    def colliding(self):
        distance_vector = Vector((self.obj_2.pos)) - Vector((self.obj_1.pos))
        distance = distance_vector.length()
        if distance <= self.obj_1.radius + self.obj_2.radius: # bounds, tuple of left edge, right edge, top and bottom
            return True
        return False

#############################################################################################
# Global Vars
p = Vector((100,200))
v = Vector((0,-0.5))
player = Player(p, v, 50,IMG,1,1)
plat = Platform(HEIGHT-100, 1, 'red')
i = Interaction(plat, player)

#############################################################################################
# Game Logic

###############
# Handlers
def draw_handler(canvas):
    global WIDTH, HEIGHT, sprite,count
    if (count % 5 == 0):
        #sprite.step_frame()
        pass
    #sprite.draw(canvas, Vector((WIDTH / 2, HEIGHT / 2)), (200, 200))
    count += 1
    i.draw(canvas)
    i.update()

def key_down_handler(key):
    player.add_move(key)

def key_up_handler(key):
    player.remove_move(key)

def timer_handler():
    global clock
    clock += 1

###############
# Rest of Code
timer = simplegui.create_timer(1, timer_handler)
timer.start()

frame = simplegui.create_frame('Testing', WIDTH, HEIGHT)
frame.set_draw_handler(draw_handler)
frame.set_keydown_handler(key_down_handler)
frame.set_keyup_handler(key_up_handler)
frame.start()

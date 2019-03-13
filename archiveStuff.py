<<<<<<< HEAD
=======
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
>>>>>>> df0f774c3605c0d21c4cbb6c4b6c8af49be4d7c3
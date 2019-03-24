from sprite import *

class Sprite_Sheet(Sprite):
    def __init__(self, frame_index = [0,0]):
        self.IMG = 'https://i.postimg.cc/xCX8fC0X/blink-sprites.png'
        self.columns = 9
        self.rows = 9
        super().__init__(self.IMG, self.columns , self.rows,frame_index)

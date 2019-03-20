from sprite import *

class Sprite_Sheet:
    def __init__(self):
        self.IMG = 'https://i.postimg.cc/pVBZVTKm/blink-sprites.png'
        self.columns = 9
        self.rows = 7
        self.sprite = Sprite(self.IMG, self.columns , self.rows)

    def draw(self,canvas, position, dimensions, frame_index):
        self.sprite.draw(canvas, position, dimensions, frame_index)


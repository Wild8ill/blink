from sprite import *

class Sprite_Sheet(Sprite):
    def __init__(self):
        self.IMG = 'https://i.postimg.cc/6qJ25Kz6/blink-sprites.png'
        self.columns = 9
        self.rows = 9
        super().__init__(self.IMG, self.columns , self.rows)

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class Sprite:
    def __init__(self, image, columns, rows):
        self.image = simplegui.load_image(image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.columns = columns
        self.rows = rows
        self.frameSize = (self.width // columns, self.height // rows)
        self.frameCentre = (self.frameSize[0] / 2, self.frameSize[1] / 2)
        self.frame_index = [0,0]

    def step_frame(self):
        self.frame_index[0] = (self.frame_index[0] + 1) % self.columns
        if self.frame_index[0] == 0:
            self.frame_index[1] = (self.frame_index[1] + 1) % self.rows

    def set_frame(self, list):
        self.frame_index = list

    def draw(self, canvas, pos, size,):
        centerSource = [self.frameSize[i] * self.frame_index[i] + self.frameCentre[i] for i in [0, 1]]
        sizeSource = self.frameSize
        centerDest = pos.getP()
        sizeDest = size
        canvas.draw_image(self.image, centerSource, sizeSource, centerDest, sizeDest)

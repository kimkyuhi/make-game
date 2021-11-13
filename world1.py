from pico2d import *

class World1:
    def __init__(self):
        self.image = load_image('world1.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 800, 480, 400, 240)
        #self.image.draw(1200, 30)

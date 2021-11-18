from pico2d import *
import game_world
import random

class Qbox:
    image = None

    def __init__(self):
        if Qbox.image == None:
            Qbox.image = load_image('questionbox.png')
        self.x, self.y = random.randint(0, 1600-1), 50

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)

from pico2d import *
import game_world

class Fire_Ball:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Fire_Ball.image == None:
            Fire_Ball.image = load_image('fireball.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x += self.velocity

        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)

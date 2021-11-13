import random
import json
import os

from pico2d import *
import game_framework
import game_world

from new_mario import Mario
from world1 import World1


name = "MainState"

new_mario = None

def enter():
    global new_mario
    new_mario = Mario()
    world1 = World1()
    game_world.add_object(world1, 0)
    game_world.add_object(new_mario, 1)


def exit():
    game_world.clear()

def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            new_mario.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()
    delay(0.01)
    # fill here


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()







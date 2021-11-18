import random
import json
import os

from pico2d import *
import game_framework
import game_world

from new_mario import Mario
from world1 import World1
from box import Qbox


name = "MainState"

new_mario = None
world1 = None
Qboxes = []


def collide(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b:
        return False
    if right_a < left_b:
        return False
    if top_a < bottom_b:
        return False
    if bottom_a > top_b:
        return False

    return True

def enter():
    global new_mario
    global world1

    new_mario = Mario()
    world1 = World1()
    global Qboxes
    Qboxes = [Qbox() for i in range(10)]
    game_world.add_objects(Qboxes, 1)
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
    for box in Qboxes:
        if collide(new_mario, box):
            Qboxes.remove(box)
            game_world.remove_object(box)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()







import random
import json
import os

from pico2d import *

import game_framework
import title_state

SCREEN_X = 1280
SCREEN_Y = 720

name = "MainState"

MAPMOVE = 0
boy = None
back = None
font = None

class Back:
    global MAPMOVE
    def __init__(self):
        self.image = load_image('MAP_1.png')

    def draw(self):
        self.image.clip_draw_to_origin(0 + MAPMOVE, 0, SCREEN_X , SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)


class Boy:
    def __init__(self):
        self.x, self.y = 0, 110
        self.speed = 5
        self.frame = 0
        self.image = load_image('Father_sprite.png')
        self.dir = 0
        self.frame_time = 0

    def update(self):
        global MAPMOVE
        if self.dir and self.frame_time % 5 == 0:
            self.frame = self.frame % 6 + 1

        if self.speed:
            self.frame_time = self.frame_time + 1

        if self.frame_time % 4 == 0:
            self.x += self.dir * self.speed

        MAPMOVE += self.dir * self.speed

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(self.frame * 80, 200, 70, 100, self.x, self.y)
        elif self.dir == -1:
            self.image.clip_draw(self.frame * 80, 0, 70, 100, self.x, self.y)

def enter():
    global boy, back
    boy = Boy()
    back = Back()

def handle_events():
    global boy

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                boy.dir = -1
                boy.speed = 5
            elif event.key == SDLK_RIGHT:
                boy.dir = 1
                boy.speed = 5
            elif event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)
        elif event.type == SDL_KEYUP:
            boy.frame = 0
            boy.speed = 0

def exit():
    global boy, back
    del (boy)
    del (back)

def pause():
    pass


def resume():
    pass

def update():
    boy.update()

def draw():
    clear_canvas()
    back.draw()
    boy.draw()
    update_canvas()






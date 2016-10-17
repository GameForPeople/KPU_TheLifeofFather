import random
import json
import os

from pico2d import *

import game_framework
import title_state

SCREEN_X = 1280
SCREEN_Y = 720

name = "MainState"

GAME_VIEW = 0 # 0일때 줌 연출 , 1 일때 0에서 2로 가는단계, 2일때!!

view_change = 0
change_rate = 20    #바꿀시 오작동 무조건 20고정
change_balance = 5  #가로 비율 속도 차치에 따른 어쩔 수 없는 변수

BOYSPEED = 3
MAPMOVE = 0

boy = None
back = None
font = None

class Back:
    global MAPMOVE
    def __init__(self):
        self.image = load_image('MAP_1.png')
        self.image_front = load_image('MAP_1_front.png')
        self.grid_img = load_image('grid.png')

    def draw(self):
        if GAME_VIEW == 0:
            self.image.clip_draw_to_origin(160,140, 580, 340, 0, 0, SCREEN_X, SCREEN_Y)
        elif GAME_VIEW == 1:
            self.image.clip_draw_to_origin(160 - (int)(160 / change_rate) * view_change,140 - (int)(140 / change_rate) * view_change , 580 + (int)( 700 / change_rate) * view_change, 340 + (int)( 380 / change_rate) * view_change, 0, 0, SCREEN_X, SCREEN_Y)
        elif GAME_VIEW == 2:
            self.image.clip_draw_to_origin(0 + MAPMOVE, 0, SCREEN_X , SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)

    def draw_front(self):
        if GAME_VIEW == 0:
            self.image_front.clip_draw_to_origin(160,140, 580, 340, 0, 0, SCREEN_X, SCREEN_Y)
        elif GAME_VIEW == 1:
            self.image_front.clip_draw_to_origin(160 - (int)(160 / change_rate) * view_change,140 - (int)(140 / change_rate) * view_change , 580 + (int)( 700 / change_rate) * view_change, 340 + (int)( 380 / change_rate) * view_change, 0, 0, SCREEN_X, SCREEN_Y)
        elif GAME_VIEW == 2:
            self.image_front.clip_draw_to_origin(0 + MAPMOVE, 0, SCREEN_X , SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)

    def make_grid(self):
        self.grid_img.clip_draw_to_origin(0, 0, SCREEN_X , SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)

class Boy:
    def __init__(self):
        self.x, self.y = 470, 195 #120
        self.speed = BOYSPEED
        self.frame = 0
        self.image = load_image('youngFather_character_sprite.png')
        self.dir = -1
        self.frame_time = 0

    def update(self):
        global MAPMOVE

        if self.speed:
            self.frame_time = self.frame_time + 1       #단위 시간을 올려줍니다.

        if self.speed and self.frame_time % 5 == 0:     #조각을 결정합니다 . 5프레이망 1번씩 이미지를 변환
            self.frame = self.frame % 6 + 1

        #if self.frame_time % 4 == 0:
        self.x += self.dir * self.speed             #1번의 단위시간동안 1번 이동합니다.

        if GAME_VIEW == 2 and self.x > 450:
            MAPMOVE += self.dir * self.speed                #수정필요

    def max_XY(self):
        if GAME_VIEW == 2 and self.x < 450:
            self.x = 450

    def control_Y(self):
        if GAME_VIEW == 2:
            if self.x < 530:
                self.y = 195
            elif self.x >  530 and self.x <= 560:
                self.y = 160
            elif self.x > 560:
                self.y = 120

    def draw(self):
        #self.print(self.x , self.y)

        if GAME_VIEW == 0:
            if self.dir == 1:
                self.image.clip_draw_to_origin(self.frame * 80, 200, 70, 100, 595, 25, 150, 220)
            elif self.dir == -1:
                self.image.clip_draw_to_origin(self.frame * 80, 0, 70, 100, 595, 25, 150, 220)
        elif GAME_VIEW == 1:
            if self.dir == 1:
                self.image.clip_draw_to_origin(self.frame * 80, 200, 70, 100, 595 - change_balance -(int)(160 / change_rate)*view_change, 25 + (int)(120 / change_rate)* view_change, 150 - (int)(80 / change_rate)* view_change, 220 - (int)(120 / change_rate)* view_change )
            elif self.dir == -1:
                self.image.clip_draw_to_origin(self.frame * 80, 0, 70, 100, 595 - change_balance - (int)(160 / change_rate)*view_change, 25 + (int)(120 / change_rate)* view_change, 150 - (int)(80 / change_rate)* view_change, 220 - (int)(120 / change_rate)* view_change )
        elif GAME_VIEW == 2:
            if self.dir == 1:
                self.image.clip_draw(self.frame * 80, 200, 70, 100, self.x, self.y) # 470, 195
            elif self.dir == -1:
                self.image.clip_draw(self.frame * 80, 0, 70, 100, self.x, self.y) # 470, 195

def handle_view():
    global view_change
    global GAME_VIEW
    global change_rate
    global change_balance

    if GAME_VIEW == 1:
        if view_change < change_rate:

            #쓰레기 코드의 시작 -> 어쩔수 없음

           if view_change == 2:
                change_balance = 11
           elif view_change == 3:
                change_balance = 21
           elif view_change == 4:
                change_balance = 24
           elif view_change == 5:
                change_balance = 26
           elif view_change == 6:
                change_balance = 28
           elif view_change == 7:
                change_balance = 30
           elif view_change == 8:
                change_balance = 31
           elif view_change == 11:
                change_balance = 31
           elif view_change == 12:
                change_balance = 28
           elif view_change == 13:
                change_balance = 24
           elif view_change == 15:
                change_balance = 23
           elif view_change == 16:
                change_balance = 20
           elif view_change == 17:
                change_balance = 15
           elif view_change == 18:
                change_balance = 9
           elif view_change == 19:
                change_balance = 7
           view_change =  view_change + 1

        if view_change == change_rate:
           #view_change = 0
           GAME_VIEW = 2

def enter():
    global boy, back
    boy = Boy()
    back = Back()

def handle_events():
    global boy
    global GAME_VIEW
    global view_change

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if GAME_VIEW < 2:
                view_change = view_change + 1
                if GAME_VIEW == 0:
                    GAME_VIEW = GAME_VIEW + 1
            if event.key == SDLK_LEFT:
                boy.dir = -1
                boy.speed = BOYSPEED
            elif event.key == SDLK_RIGHT:
                boy.dir = 1
                boy.speed = BOYSPEED
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
    boy.max_XY()
    boy.control_Y()
    handle_view()

def draw():
    clear_canvas()
    back.draw()
    boy.draw()
    back.draw_front()
    back.make_grid()
    update_canvas()






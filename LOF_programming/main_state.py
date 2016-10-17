import random
import json
import os

from pico2d import *

import game_framework
import title_state

MAGIC_X1 = 1380      # DISTANCE 가로등 1 ~ 가로등 2
count_x1 = 0         # MAGIC_X1 측정
RESULT_X1 = 2190     # 2190 일때 MAP_MOVE 초기화

SCREEN_X = 1280
SCREEN_Y = 720

BOY_SPEED = 3
MAP_MOVE = 0

name = "MainState"

GAME_VIEW = 0 # 0일때 줌 연출 , 1 일때 0에서 2로 가는단계, 2일때!!, 3이 가로등 , 4가 가로등으로인한 시점, 5가 중앙 6이 가로등 꺼짐

view_change = 0
change_rate = 20    #바꿀시 오작동!!! 무조건 20고정
change_balance = 5  #가로 비율 속도 차치에 따른 어쩔 수 없는 변수 의 초기값!! 바꿀시 오작동!!


boy = None
back = None
font = None
object_light = None

class Object_list:
    def __init__(self):
        self.x = 795
        self.y = 218
        self.onoff_1 = 0
        self.onoff_1_timer = 0
        self.onoff_2 = 0
        self.onoff_3 = 0
        self.onoff_count = 0
        self.image = load_image('Light_1.png')

    def draw(self):
        global MAP_MOVE
        global MAGIC_X1

        if self.onoff_1 == 1:
            self.image.draw(self.x - MAP_MOVE , self.y, 262, 291)

        if self.onoff_2 == 1:
            self.image.draw(self.x + MAGIC_X1 - MAP_MOVE + 8, self.y, 262, 291)

    def update(self):
        global GAME_VIEW

        if self.onoff_2 == 1 and self.onoff_1_timer < 30:
            self.onoff_1_timer = self.onoff_1_timer + 1

            if self.onoff_1_timer % 10 < 5:
                self.onoff_1 = 1
            elif self.onoff_1_timer % 10 >= 5:
                self.onoff_1 = 0

            if self.onoff_1_timer == 30:
                self.onoff_1 = 1
                GAME_VIEW = 3
class Back:
    global MAP_MOVE
    global RESULT_X1
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
            self.image.clip_draw_to_origin(0, 0, SCREEN_X , SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)
        elif GAME_VIEW == 3 or GAME_VIEW == 4 or GAME_VIEW == 5:
            self.image.clip_draw_to_origin(0 + MAP_MOVE, 0, SCREEN_X, SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)
        elif GAME_VIEW == 6:
            self.image.clip_draw_to_origin(RESULT_X1 - 640 + MAP_MOVE, 0, SCREEN_X, SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)

    def draw_front(self):
        if GAME_VIEW == 0:
            self.image_front.clip_draw_to_origin(160,140, 580, 340, 0, 0, SCREEN_X, SCREEN_Y)
        elif GAME_VIEW == 1:
            self.image_front.clip_draw_to_origin(160 - (int)(160 / change_rate) * view_change,140 - (int)(140 / change_rate) * view_change , 580 + (int)( 700 / change_rate) * view_change, 340 + (int)( 380 / change_rate) * view_change, 0, 0, SCREEN_X, SCREEN_Y)
        elif GAME_VIEW == 2:
            self.image_front.clip_draw_to_origin(0, 0, SCREEN_X , SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)
        elif GAME_VIEW == 3 or GAME_VIEW == 4 or GAME_VIEW == 5:
            self.image_front.clip_draw_to_origin(0 + MAP_MOVE, 0, SCREEN_X, SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)
        elif GAME_VIEW == 6:
            self.image_front.clip_draw_to_origin(RESULT_X1 - 640 + MAP_MOVE, 0, SCREEN_X, SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)

    def make_grid(self):
        self.grid_img.clip_draw_to_origin(0, 0, SCREEN_X , SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)

class Boy:
    def __init__(self):
        self.x, self.y = 470, 195 #120
        self.speed = BOY_SPEED
        self.frame = 0
        self.image = load_image('youngFather_character_sprite.png')
        self.dir = -1
        self.frame_time = 0

    def update(self):
        global MAP_MOVE
        global GAME_VIEW
        global object_light
        global count_x1
        global MAGIC_X1

        self.x += self.dir * self.speed  # 1번의 단위시간동안 1번 이동합니다.

        if self.speed:
            self.frame_time = self.frame_time + 1       #단위 시간을 올려줍니다.

        if self.speed and self.frame_time % 5 == 0:     #조각을 결정합니다 . 5프레임 1번씩 이미지를 변환
            self.frame = self.frame % 6 + 1

        if GAME_VIEW == 4 or GAME_VIEW == 5:            # 가로등과 가로등 사이에 거리를 체크합니다.
            count_x1 = count_x1 + self.dir * self.speed
            if GAME_VIEW == 5 and count_x1 >= MAGIC_X1 - 5 and count_x1 <= MAGIC_X1 + 5:
                GAME_VIEW = 6
                object_light.onoff_1 = 0
                object_light.onoff_2 = 0
                object_light.onoff_count = object_light.onoff_count + 1

                self.x = 640
                MAP_MOVE = 0

        if GAME_VIEW == 5 or GAME_VIEW == 6:
            MAP_MOVE = MAP_MOVE + self.dir * self.speed

        if GAME_VIEW == 4 and self.x < 200 and self.speed:
            self.x = 200 #self.speed               #수정필요

        elif GAME_VIEW == 4 and self.x > 635 and self.x < 645:
            GAME_VIEW = 5
            self.x = 640

        elif GAME_VIEW == 2 and self.x > 795 and self.x < 805:
            self.x = 800
            #GAME_VIEW = 3
            object_light.onoff_1 = 1
            object_light.onoff_2 = 1
            object_light.onoff_count = object_light.onoff_count + 1

    def max_XY(self): #??? 이 함수 어따쓰는거지??? 뭐야
        if GAME_VIEW == 2 and self.x < 450:
            self.x = 450

    def control_Y(self):
        if GAME_VIEW == 2:
            if self.x <= 595:
                self.y = 195
            elif self.x > 595 and self.x <= 645:
                self.y = 160
            elif self.x > 645:
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
        elif GAME_VIEW == 3 or GAME_VIEW == 4:
            if self.dir == 1:
                self.image.clip_draw(self.frame * 80, 200, 70, 100, self.x, self.y)
            elif self.dir == -1:
                self.image.clip_draw(self.frame * 80, 0, 70, 100, self.x, self.y)
        elif GAME_VIEW == 5 or GAME_VIEW == 6:
            if self.dir == 1:
                self.image.clip_draw(self.frame * 80, 200, 70, 100, 640, self.y)
            elif self.dir == -1:
                self.image.clip_draw(self.frame * 80, 0, 70, 100, 640, self.y)
        elif GAME_VIEW == 6:
            if self.dir == 1:
                self.image.clip_draw(self.frame * 80, 200, 70, 100, self.x, self.y)
            elif self.dir == -1:
                self.image.clip_draw(self.frame * 80, 0, 70, 100, self.x, self.y)


def handle_view():
    global view_change
    global GAME_VIEW
    global change_rate
    global change_balance
    global MAP_MOVE
    global boy


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

    elif GAME_VIEW == 3:
        MAP_MOVE = MAP_MOVE + 10
        boy.x = boy.x - 10

        if MAP_MOVE == 600:
            GAME_VIEW = 4



def enter():
    global boy, back, object_light
    boy = Boy()
    back = Back()
    object_light = Object_list()

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
                boy.speed = BOY_SPEED
            elif event.key == SDLK_RIGHT:
                boy.dir = 1
                boy.speed = BOY_SPEED
            elif event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)
        elif event.type == SDL_KEYUP:
            boy.frame = 0
            boy.speed = 0

def exit():
    global boy, back, object_light
    del (boy)
    del (back)
    del (object_light)

def pause():
    pass


def resume():
    pass

def update():
    boy.update()
    boy.max_XY()
    boy.control_Y()
    object_light.update()
    handle_view()

def draw():
    clear_canvas()
    back.draw()
    boy.draw()
    object_light.draw()
    back.draw_front()
    back.make_grid()
    update_canvas()






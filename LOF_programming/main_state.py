import random
import json
import os

from pico2d import *

import game_framework
import main_state_2
import title_state


SCREEN_X = 1280         # 화면 X축 고정 크기
SCREEN_Y = 720          # 화면 Y축 고정 크기

MAGIC_X1 = 1380      # DISTANCE 가로등 1 ~ 가로등 2 //절대좌표
RESULT_X1 = 2190     # 2190 일때 MAP_MOVE 초기화
count_x1 = 0         # MAGIC_X1 측정 -> 버그있으니 수정이 필요함 -> 플레이어의 컨트롤 권한을 뻇으면 해결할 수 있는 문제라고 생각됨

FATHER_SPEED = 3       # 남자 어른의 스피드는 3으로 설정합니다. -> 애기 1/2, 유치원 1, 남자 노인 2, 남자 어른 3, 학생 6
MAP_MOVE = 0        # 맵의 움직임을 통해 카메라 연출 목적으로 사용됨

name = "MainState"

GAME_VIEW = 0 # 0일때 줌 연출 , 1 일때 0에서 2로 가는단계, 2일때!!, 3이 가로등 , 4가 가로등으로인한 시점, 5가 중앙 6이 가로등 꺼짐 7일때, 화면 반으로 조절


BUS_START_X = -150
BUS_START_Y = 180

PEOPLE_START_X = 2750
PEOPLE_START_y = 65

LIGHT_START_X = 795
LIGHT_START_Y = 218
LIGHT_ONOFF_SETTING = 0


view_change = 0
change_rate = 20    # 바꿀시 오작동!!! 무조건 20고정
change_balance = 5  # 가로 비율 속도 차치에 따른 어쩔 수 없는 변수 의 초기값!! 바꿀시 오작동!!

grid_button = 0
bus_button = 0
view_8_speed = 2
view_9_speed = 2
handle_count = 0
time_check = 0

father = None
back = None
font = None
bgm = None
dialog = None
object_light = None
object_bus = None
object_people = None
movie = None


class Movie:
    def __init__(self):
        self.button = 1

    def update(self):
        global GAME_VIEW, object_light, father

        if GAME_VIEW == 2 and object_light.onoff_1 == 0:
            father.dir = 1
            father.speed = FATHER_SPEED
        elif GAME_VIEW == 4 or GAME_VIEW == 5 or GAME_VIEW == 6:
            father.dir = 1
            father.speed = FATHER_SPEED
        else:
            father.speed = 0
            father.frame = 0


class Dialog:
    def __init__(self):
        self.x = 640
        self.y = 500
        self.count = 1
        self.time_count = 0
        self.image_1 = load_image('Resource\Image\Main_state\dialog_2.png')
        self.image_2 = load_image('Resource\Image\Main_state\dialog_1.png')
        self.image_3 = load_image('Resource\Image\Main_state\dialog_3.png')
        self.image_4 = load_image('Resource\Image\Main_state\dialog_4.png')
        self.image_5 = load_image('Resource\Image\Main_state\dialog_5.png')
        self.image_6 = load_image('Resource\Image\Main_state\dialog_6.png')
        self.image_7 = load_image('Resource\Image\Main_state\dialog_7.png')
        self.image_8 = load_image('Resource\Image\Main_state\dialog_8.png')

        self.button = 0
        self.timing = 0
        self.x_5 = 0

    def update(self):
        global GAME_VIEW, father, view_change
        if self.button == 0:
            self.timing += 1

        if GAME_VIEW == 4 and self.timing > 50:    #GAME_VIEW 가 4일떄 다음 다이얼로그를 띄워야하므로! 타이밍 지수를 초기화해줌!
            self.timing = 0

        elif GAME_VIEW == 5 and self.timing > 50:    #GAME_VIEW 가 4일떄 다음 다이얼로그를 띄워야하므로! 타이밍 지수를 초기화해줌!
            self.timing = 0

        elif GAME_VIEW == 9 and self.timing > 300:    #GAME_VIEW 가 4일떄 다음 다이얼로그를 띄워야하므로! 타이밍 지수를 초기화해줌!
            self.timing = 0

        ##print(self.timing)

        if self.count == 1 and self.timing == 10 and self.time_count == 0:
            self.button = 1
            self.timing = 0

        elif self.count == 2 and self.timing == 10 and self.time_count == 0:
            self.button = 1
            self.timing = 0

        elif self.count == 3 and self.timing == 10 and self.time_count == 0:
            self.button = 1
            self.timing = 0

        elif GAME_VIEW == 4 and self.count == 4 and self.timing == 10 and self.time_count == 0:
            self.button = 1
            self.timing = 0
            self.y = 200
            self.x = 440

        elif GAME_VIEW == 5 and self.count == 5 and self.timing >= 5 and self.time_count == 0:
            self.button = 1
            self.timing = 0
            self.y = 200
            self.x_5 = 750

        elif GAME_VIEW == 5 and self.count == 6 and self.timing >= 10 and self.time_count == 0:
            self.button = 1
            self.timing = 0
            self.y = 200
            self.x_5 = 750

        elif GAME_VIEW == 9 and self.count == 7 and self.timing >= 150 and self.time_count == 0:
            self.button = 1
            self.timing = 0
            self.y = 350
            self.x = 640

        elif GAME_VIEW == 10 and self.count == 8 and self.timing >= 50 and self.time_count == 0:
            self.button = 1
            self.timing = 0
            self.y = 350
            self.x = 640

        if self.button > 0:
            if GAME_VIEW == 5:
                self.x_5 += father.speed * (-1) * father.dir

        if self.button == 1:
            self.time_count += 1


            if self.time_count >= 80:
                self.button = 2

        elif self.button == 2:
            self.time_count -= 1

            if self.time_count <= 0:  #조작하고 싶으면 여기서 하셔!!!
                if self.count == 3:
                    if GAME_VIEW < 2:
                        view_change = view_change + 1
                        if GAME_VIEW == 0:
                            GAME_VIEW = GAME_VIEW + 1
                if self.count == 8:
                    GAME_VIEW = 11
                self.count += 1
                self.button = 0

    def draw(self):
        for i in range( 1, (int)((self.time_count) / 5) , 1):
            if self.count == 1:
                self.image_1.draw(self.x, self.y, 1000, 200)
            elif self.count == 2:
                self.image_2.draw(self.x, self.y, 1000, 200)
            elif self.count == 3:
                self.image_3.draw(self.x, self.y, 1000, 200)
            elif self.count == 4:
                self.image_4.draw(self.x, self.y, 1000, 200)
            elif self.count == 5:
                self.image_5.draw(self.x_5, self.y, 1000, 200)
            elif self.count == 6:
                self.image_6.draw(self.x_5, self.y, 1000, 200)
            elif self.count == 7:
                self.image_7.draw(self.x, self.y, 1000, 200)
            elif self.count == 8:
                self.image_8.draw(self.x, self.y, 1000, 200)


class Object_people:
    def __init__(self):
        self.x = PEOPLE_START_X
        self.y = PEOPLE_START_y
        self.timer = 0
        self.image = load_image('Resource\Image\Main_state\people_1.png')
        self.clipping = 0

    def draw(self):
        #self.image.draw(self.x, self.y, 152, 117)
        self.image.clip_draw_to_origin(0, 0, 152 - self.clipping, 117, self.x, self.y)
    def update(self):
        global father
        global object_bus

        if GAME_VIEW == 5:
            self.x = 2750 - father.x  #father.dir * father_SPEED

        if GAME_VIEW == 8:
            self.x -= view_8_speed

        if object_bus.speed == 0:
            self.timer += 1

            if self.timer == 60:
                self.timer = 0
                self.clipping += 50
                self.x += 50


class Object_bus:

    def __init__(self):
        self.x = BUS_START_X
        self.y = BUS_START_Y
        self.timer = 0
        self.speed = 6
        self.timer_2 = 0
        self.image_type = 0
        self.image = load_image('Resource\Image\Main_state\BUS_1.png')
        self.image_2 = load_image('Resource\Image\Main_state\BUS_2.png')
        self.image_3 = load_image('Resource\Image\Main_state\BUS_3.png')
        self.image_4 = load_image('Resource\Image\Main_state\BUS_4.png')

    def draw(self):
        if self.image_type == 0:
            self.image.draw(self.x, self.y, 372, 230)
        elif self.image_type == 1 or self.image_type == 2:
            self.image_2.draw(self.x, self.y, 372, 230)
        elif self.image_type == 3:
            self.image_3.draw(self.x, self.y, 372, 230)
        elif self.image_type == 4 or self.image_type == 5:
            if GAME_VIEW > 8:
                self.image_4.clip_draw_to_origin(0,0, 372, 230, self.x - 186 - handle_count * 2, self.y - 115 - (int)(handle_count / 8), 372 + 4 * handle_count, 230 + 2*handle_count)
                # self.image.clip_draw_to_origin(RESULT_X1 - 640 + MAP_MOVE + 2 * handle_count, 0 + (int)(handle_count / 4) , SCREEN_X - 2 * handle_count, SCREEN_Y - 2 * handle_count, 0, 0, SCREEN_X, SCREEN_Y)

            else:
                self.image_4.draw(self.x, self.y, 372, 230)

    def stop(self):
        self.speed = 0

    def update(self):
        global GAME_VIEW
        global view_8_speed
        global MAP_MOVE

        self.x += self.speed
        self.timer += 1

        if self.x > 630 and self.x < 640:
            GAME_VIEW = 8
            self.timer = 0

        if self.timer == 20 and GAME_VIEW == 8 and self.speed != 0:
            self.speed -= 1
            self.timer = 0
         #   if(self.speed == 0):

        if self.speed == 0 and GAME_VIEW == 8:
            self.timer_2 += 1

            if self.timer_2 == 60:
                self.timer_2 = 0
                self.image_type += 1
                if self.image_type == 5:
                    GAME_VIEW = 9

        if self.speed == 0:
            self.x -= view_8_speed # 2는 맵무브 스피드!!!
            if self.x == 640:
                view_8_speed = 0


class Object_light:
    def __init__(self):
        self.x = LIGHT_START_X
        self.y = LIGHT_START_Y
        self.onoff_1 = LIGHT_ONOFF_SETTING
        self.onoff_1_timer = LIGHT_ONOFF_SETTING
        self.onoff_2 = LIGHT_ONOFF_SETTING
        self.onoff_3 = LIGHT_ONOFF_SETTING
        self.onoff_count = LIGHT_ONOFF_SETTING
        self.image = load_image('Resource\Image\Main_state\Light_1.png')

    def draw(self):
        global MAP_MOVE
        global MAGIC_X1

        if self.onoff_1 == 1:
            self.image.draw(self.x - MAP_MOVE , self.y, 262, 291)

        if self.onoff_2 == 1:
            self.image.draw(self.x + MAGIC_X1 - MAP_MOVE + 8, self.y, 262, 291)

    def update(self):
        global GAME_VIEW

        delay(0.02)

        if self.onoff_2 == 1 and self.onoff_1_timer < 30:
            self.onoff_1_timer += 1

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
        self.image = load_image('Resource\Image\Main_state\MAP_1_bus.png')
        self.image_front = load_image('Resource\Image\Main_state\MAP_1_front_bus.png')
        self.grid_img = load_image('Resource\Image\grid.png')
        self.black_down = load_image('Resource\Image\Main_state\_black_down_animation.png')
        self.black_down_timer = 0
        self.black_down_screen = 1

        self.thanks_img = load_image('Resource\Image\Main_state\_thanksto.png')

    def black_down_animation(self):
        self.black_down.clip_draw_to_origin(0, 0 + self.black_down_timer, 1280, 720 + self.black_down_timer, 0, 720 - self.black_down_screen , 1280, self.black_down_screen)

    def black_down_animation_tiemr(self):
        global GAME_VIEW

        if GAME_VIEW == 11:
            if self.black_down_timer < 1440:
                self.black_down_timer += 20

            if self.black_down_screen < 720:
                self.black_down_screen += 20

            if self.black_down_timer >= 1440:
                game_framework.change_state(main_state_2)
    def draw(self):
        global handle_count

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
        elif GAME_VIEW == 7:
            self.image.clip_draw_to_origin(RESULT_X1 - 640 + MAP_MOVE, 0, SCREEN_X, SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)
        elif GAME_VIEW == 8:
            self.image.clip_draw_to_origin(RESULT_X1 - 640 + MAP_MOVE, 0, SCREEN_X, SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)
        elif GAME_VIEW == 9:
            self.image.clip_draw_to_origin(RESULT_X1 - 640 + MAP_MOVE + 2 * handle_count, 0 + (int)(handle_count / 4) , SCREEN_X - 2 * handle_count, SCREEN_Y - 2 * handle_count, 0, 0, SCREEN_X, SCREEN_Y)
        elif GAME_VIEW >= 10:
            self.image.clip_draw_to_origin(RESULT_X1 - 640 + MAP_MOVE + 2 * handle_count,0 + (int)(handle_count / 4) , SCREEN_X - 2 * handle_count, SCREEN_Y - 2 * handle_count, 0, 0, SCREEN_X, SCREEN_Y)

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
            #self.thanks_img.clip_draw_to_origin(0, 0, SCREEN_X, SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)
        elif GAME_VIEW == 7:
            self.image_front.clip_draw_to_origin(RESULT_X1 - 640 + MAP_MOVE, 0, SCREEN_X, SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)
        elif GAME_VIEW == 8:
            self.image_front.clip_draw_to_origin(RESULT_X1 - 640 + MAP_MOVE, 0, SCREEN_X, SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)
        elif GAME_VIEW == 9:
            self.image_front.clip_draw_to_origin(RESULT_X1 - 640 + MAP_MOVE + 2 * handle_count, 0 + (int)(handle_count / 4) , SCREEN_X - 2 * handle_count, SCREEN_Y - 2 * handle_count, 0, 0, SCREEN_X, SCREEN_Y)
        elif GAME_VIEW >= 10:
            self.image_front.clip_draw_to_origin(RESULT_X1 - 640 + MAP_MOVE + 2 * handle_count, 0 + (int)(handle_count / 4) , SCREEN_X - 2 * handle_count, SCREEN_Y - 2 * handle_count, 0, 0, SCREEN_X, SCREEN_Y)

    def make_grid(self):
        if grid_button == 1:
                self.grid_img.clip_draw_to_origin(0, 0, SCREEN_X , SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)


class Father:

    image = None

    def __init__(self):
        self.x, self.y = 470, 195 #120
        self.speed = 0
        self.frame = 0
        self.image = load_image('Resource\Image\Main_state\youngFather_character_sprite.png')
        self.dir = -1
        self.frame_time = 0
        self.frame_off = 0
        self.timer = 0
        self.count = 0
        self.draw_off = 0

    def update(self):
        global MAP_MOVE
        global GAME_VIEW
        global object_light
        global object_bus
        global count_x1
        global MAGIC_X1
        global bus_button
        global view_8_speed

        self.x += self.dir * self.speed  # 1번의 단위시간동안 1번 이동합니다.

        if self.speed:
            self.frame_time = self.frame_time + 1       #단위 시간을 올려줍니다.

        if self.speed and self.frame_time % 5 == 0:     #조각을 결정합니다 . 5프레임 1번씩 이미지를 변환
            self.frame = self.frame % 6 + 1
        if object_bus.speed == 0:
            self.timer += 1
            if self.timer == 60 and self.count < 4:
                self.timer = 0
                self.count += 1
                self.x += 75

            if self.count == 4:
                self.draw_off = 1

        if GAME_VIEW == 3 or GAME_VIEW == 4 or GAME_VIEW == 5:            # 가로등과 가로등 사이에 거리를 체크합니다.
            count_x1 = count_x1 + self.dir * self.speed
            if GAME_VIEW == 5 and count_x1 >= MAGIC_X1 - 5 and count_x1 <= MAGIC_X1 + 5:
                GAME_VIEW = 6
                object_light.onoff_1 = 0
                object_light.onoff_2 = 0
                object_light.onoff_count = object_light.onoff_count + 1
                self.x = 640
                MAP_MOVE = 0

        if GAME_VIEW == 5:
            MAP_MOVE = MAP_MOVE + self.dir * self.speed

        elif GAME_VIEW == 6:
            #MAP_MOVE = MAP_MOVE + (int)(self.dir * self.speed / 2 )
            if self.x > 1000 and self.x < 1005:
                GAME_VIEW = 7
                bus_button = 1

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

        elif GAME_VIEW == 8:
            self.x -= view_8_speed
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
        if self.draw_off == 0:
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
            elif GAME_VIEW == 5:
                if self.dir == 1:
                    self.image.clip_draw(self.frame * 80, 200, 70, 100, 640, self.y)
                elif self.dir == -1:
                    self.image.clip_draw(self.frame * 80, 0, 70, 100, 640, self.y)
            elif GAME_VIEW == 6:
                if self.dir == 1:
                    self.image.clip_draw(self.frame * 80, 200, 70, 100, self.x, self.y)
                elif self.dir == -1:
                    self.image.clip_draw(self.frame * 80, 0, 70, 100, self.x, self.y)
            elif GAME_VIEW == 7:
                if self.dir == 1:
                    self.image.clip_draw(self.frame * 80, 200, 70, 100, self.x, self.y)
                elif self.dir == -1:
                    self.image.clip_draw(self.frame * 80, 0, 70, 100, self.x, self.y)
            elif GAME_VIEW == 8:
                if self.dir == 1:
                   self.image.clip_draw(self.frame * 80, 200, 70, 100, self.x, self.y)
                elif self.dir == -1:
                   self.image.clip_draw(self.frame * 80, 0, 70, 100, self.x, self.y)


def handle_view():
    global view_change, view_change_rate
    global GAME_VIEW
    global change_rate
    global change_balance
    global MAP_MOVE
    global father
    global view_8_speed
    global view_9_speed
    global handle_count
    global time_check

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
        MAP_MOVE += + 10
        father.x += - 10

        if MAP_MOVE == 600:
            GAME_VIEW = 4

    elif GAME_VIEW == 8:
        MAP_MOVE += view_8_speed

    elif GAME_VIEW == 9:
        MAP_MOVE += view_9_speed
        handle_count += 1

        if handle_count == 10 or handle_count == 20:
            view_9_speed += 1

        # 속도가 너무 빠르면 맵밖으로 나갈 수 있어서 안됨!!
       # if handle_count == 30 or handle_count == 40 :
        #    view_9_speed += 3
        # 마지막 카메라 하이라이트를 구현하자!!!!


        if handle_count == 200:
            GAME_VIEW = 10          #마지막 카메라 하이라이트를 구현하자!!!!


    elif GAME_VIEW == 10:
        MAP_MOVE += view_9_speed
        time_check += 1
        #print(time_check)      600까지 쓸수 있음 r고마워!!

        if time_check >= 600:       #객체화를 통해 굳이 쓸모가 없어져버렷음!
            GAME_VIEW = 11

    elif GAME_VIEW == 11:
        MAP_MOVE += view_9_speed


def enter():
    global father, back, object_light, object_bus, object_people, dialog, bgm, movie
    #open_canvas()
    father = Father()
    back = Back()
    object_light = Object_light()
    object_bus = Object_bus()
    object_people = Object_people()
    dialog = Dialog()
    movie = Movie()

    bgm = load_music('Resource\Sound\Main_BGM.ogg')
    bgm.play()


def handle_events():
    global father
    global GAME_VIEW
    global view_change
    global grid_button

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if GAME_VIEW != 0 and GAME_VIEW != 1 and GAME_VIEW != 3:
                if event.key == SDLK_LEFT:
                    father.dir = -1
                    father.speed = FATHER_SPEED
                elif event.key == SDLK_RIGHT:
                    father.dir = 1
                    father.speed = FATHER_SPEED

            if event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)
            elif event.key == SDLK_g:
                if grid_button == 0:
                    grid_button = 1
                elif grid_button == 1:
                    grid_button = 0

        elif event.type == SDL_KEYUP:
            father.frame = 0
            father.speed = 0


def exit():
    global father, back, object_light, object_bus, object_people, dialog, movie
    del (father)
    del (back)
    del (object_light)
    del (object_bus)
    del (object_people)
    del (dialog)
    del (movie)

def pause():
    pass


def resume():
    pass


def update():
    father.update()
    father.control_Y()
    object_light.update()
    object_people.update()
    dialog.update()
    movie.update()

    print (GAME_VIEW)
    if bus_button == 1:
        object_bus.update()

    back.black_down_animation_tiemr()

    handle_view()


def draw():
    clear_canvas()
    back.draw()

    object_people.draw()
    father.draw()
    object_light.draw()

    if bus_button == 1:
        object_bus.draw()

    back.draw_front()
    dialog.draw()
    back.black_down_animation()
    back.make_grid()
    update_canvas()






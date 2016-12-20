import game_framework

from pico2d import *

import main_state_4

name = "Main_State_3"

SCREEN_X = 1280
SCREEN_Y = 720

FATHER_SPEED = 4
SON_SPEED = 2

grid_button = 0

father = None
son = None
back = None
effect = None
movie = None
car = None
title = None
dia = None

MODE_editor = 0


class Movie: #여기서 그냥 모든 걸 박살 내 버리자!!!암ㄴㄷ호ㅓㅏㄹ안유라ㅗㄴ아!!
    def __init__(self):
        self.button = 1
        self.timer_4 = 0

    def first_scene(self):
        global father, back, dia, MODE_editor

        if father.x > 600:
            father.dir = -1
            father.speed = FATHER_SPEED

        elif father.x <= 600:
            father.speed = 0
            #self.button = 2

            MODE_editor = 2
            dia.dia_1_button = 1

    def second_scene(self):
        global father, back

        father.frame = 0

        if back.map_move < 3600:
            back.map_move += 25

        elif back.map_move >= 3600:
            self.button = 3

    def third_scene(self):
        global son, back, MODE_editor

        if son.x < 600:
            son.dir = 1
            son.speed = SON_SPEED

            if son.x == 300:
                dia.dia_2_button = 1
                MODE_editor = 2

        elif son.x >= 600:
            son.speed = 0
            #self.button = 4
            dia.dia_3_button = 1
            MODE_editor = 2

    def scene_4(self):
        global son
        self.timer_4 += 1

        if self.timer_4 < 50:
            son.frame = 0

        if self.timer_4 >= 50:
            son.dir = 1
            son.speed = SON_SPEED
            son.y_plus -= son.speed

            if son.y < -100:
                self.button = 5

    def scene_5(self):
        global back, dia, MODE_editor

        if back.map_move > 200:
            back.map_move -= 50

        elif back.map_move <= 200:
            dia.dia_4_button = 1
            MODE_editor = 2
            #self.button = 6

    def scene_6(self):
        global back, father, son
        son.dir = 1
        son.speed = SON_SPEED
        son.y_plus -= son.speed / son.speed

        father.y_plus += FATHER_SPEED

        back.map_move += FATHER_SPEED

        if son.y < 720 and father.y > 0:
            self.button = 7

    def scene_7(self):
        global father, son, dia, MODE_editor
        son.y_plus -= son.speed / son.speed
        father.y_plus += FATHER_SPEED / FATHER_SPEED

        if son.y - father.y <= 2:
            dia.dia_5_button = 1
            MODE_editor = 2

    def Scene_type(self):
        if self.button == 1:
            Movie.first_scene(self)
        elif self.button == 2:
            Movie.second_scene(self)
        elif self.button == 3:
            Movie.third_scene(self)
        elif self.button == 4:
            Movie.scene_4(self)
        elif self.button == 5:
            Movie.scene_5(self)
        elif self.button == 6:
            Movie.scene_6(self)
        elif self.button == 7:
            Movie.scene_7(self)
        elif self.button == 8:
            game_framework.change_state(main_state_4)

class Title:
    title_img = None
    black_img = None
    first_img = None

    def __init__(self):
        self.title_img = load_image('Resource\Image\Main_state_3\_title.png')
        self.black_img = load_image('Resource\Image\Main_state_3\_black_screen_10.png')
        self.first_img = load_image('Resource\Image\Main_state_3\_first_img.png')

        self.black_timer = 15
        self.title_timer = 0

        self.all_timer = 0

        self.black_button = 1
        self.title_button = 0

    def draw(self):

        self.first_img.draw(640, 360)

        for i in range(0, self.black_timer, 1):
            self.black_img.draw(640, 360)

        for i in range(0, self.title_timer, 1):
            self.title_img.draw(640, 360)

    def update(self):
        global MODE_editor

        self.all_timer += 1

        #print(self.chapter_timer)

        if self.title_button == 0:
            if self.title_timer == 0:
                if self.all_timer == 50:
                    self.title_timer = 1
                    self.all_timer = 0
            elif self.all_timer == 5:
                self.all_timer = 0
                self.title_timer += 1

                if self.title_timer == 15:
                    self.title_button = 1

        elif self.title_button == 1:
            if self.title_timer == 15:
                if self.all_timer == 50:
                    self.title_timer = 14
                    self.all_timer = 0
            elif self.all_timer == 5:
                self.all_timer = 0
                self.title_timer -= 1

                if self.title_timer == 0:
                    self.title_button = 2

        elif self.black_button == 1:
            if self.all_timer == 5:
                self.all_timer = 0
                self.black_timer -= 1

                if self.black_timer == 0:
                    MODE_editor = 1


class Dia:
    dia_1_img = None
    dia_2_img = None
    dia_3_img = None
    dia_4_img = None
    dia_5_img = None


    def __init__(self):
        self.dia_1_img = load_image('Resource\Image\Main_state_3\dia_1.png')
        self.dia_2_img = load_image('Resource\Image\Main_state_3\dia_2.png')
        self.dia_3_img = load_image('Resource\Image\Main_state_3\dia_3.png')
        self.dia_4_img = load_image('Resource\Image\Main_state_3\dia_4.png')
        self.dia_5_img = load_image('Resource\Image\Main_state_3\dia_5.png')


        self.dia_1_timer = 0
        self.dia_2_timer = 0
        self.dia_3_timer = 0
        self.dia_4_timer = 0
        self.dia_5_timer = 0


        self.all_timer = 0

        self.dia_1_button = 0
        self.dia_2_button = 0
        self.dia_3_button = 0
        self.dia_4_button = 0
        self.dia_5_button = 0



    def draw(self):

        for i in range(0, self.dia_1_timer, 1):
            self.dia_1_img.draw(640, 360)

        for i in range(0, self.dia_2_timer, 1):
            self.dia_2_img.draw(640, 360)

        for i in range(0, self.dia_3_timer, 1):
            self.dia_3_img.draw(640, 360)

        for i in range(0, self.dia_4_timer, 1):
            self.dia_4_img.draw(640, 360)

        for i in range(0, self.dia_5_timer, 1):
            self.dia_5_img.draw(640, 360)

    def update(self):
        global MODE_editor, movie
        self.all_timer += 1

        if self.dia_1_button == 1:
            if self.dia_1_timer == 0:
                if self.all_timer == 50:
                    self.dia_1_timer = 1
                    self.all_timer = 0
            elif self.all_timer == 3:
                self.all_timer = 0
                self.dia_1_timer += 1

                if self.dia_1_timer == 20:
                    self.dia_1_button = 2

        elif self.dia_1_button == 2:
            if self.dia_1_timer == 20:
                if self.all_timer == 50:
                    self.dia_1_timer = 19
                    self.all_timer = 0
            elif self.all_timer == 3:
                self.all_timer = 0
                self.dia_1_timer -= 1

                if self.dia_1_timer == 0:
                    self.dia_1_button = 3
                    MODE_editor = 1
                    movie.button = 2

        if self.dia_2_button == 1:
            if self.dia_2_timer == 0:
                if self.all_timer == 50:
                    self.dia_2_timer = 1
                    self.all_timer = 0
            elif self.all_timer == 3:
                self.all_timer = 0
                self.dia_2_timer += 1

                if self.dia_2_timer == 30:
                    self.dia_2_button = 2

        elif self.dia_2_button == 2:
            if self.dia_2_timer == 30:
                if self.all_timer == 50:
                    self.dia_2_timer = 29
                    self.all_timer = 0
            elif self.all_timer == 3:
                self.all_timer = 0
                self.dia_2_timer -= 1

                if self.dia_2_timer == 0:
                    self.dia_2_button = 3
                    MODE_editor = 1

        if self.dia_3_button == 1:
            if self.dia_3_timer == 0:
                if self.all_timer == 50:
                    self.dia_3_timer = 1
                    self.all_timer = 0
            elif self.all_timer == 3:
                self.all_timer = 0
                self.dia_3_timer += 1

                if self.dia_3_timer == 15:
                    self.dia_3_button = 2

        elif self.dia_3_button == 2:
            if self.dia_3_timer == 15:
                if self.all_timer == 50:
                    self.dia_3_timer = 14
                    self.all_timer = 0
            elif self.all_timer == 3:
                self.all_timer = 0
                self.dia_3_timer -= 1

                if self.dia_3_timer == 0:
                    self.dia_3_button = 3
                    MODE_editor = 1
                    movie.button = 4

        if self.dia_4_button == 1:
            if self.dia_4_timer == 0:
                if self.all_timer == 50:
                    self.dia_4_timer = 1
                    self.all_timer = 0
            elif self.all_timer == 3:
                self.all_timer = 0
                self.dia_4_timer += 1

                if self.dia_4_timer == 15:
                    self.dia_4_button = 2

        elif self.dia_4_button == 2:
            if self.dia_4_timer == 15:
                if self.all_timer == 50:
                    self.dia_4_timer = 14
                    self.all_timer = 0
            elif self.all_timer == 3:
                self.all_timer = 0
                self.dia_4_timer -= 1

                if self.dia_4_timer == 0:
                    self.dia_4_button = 3
                    MODE_editor = 1
                    movie.button = 6

        if self.dia_5_button == 1:
            if self.dia_5_timer == 0:
                if self.all_timer == 50:
                    self.dia_5_timer = 1
                    self.all_timer = 0
            elif self.all_timer == 2:
                self.all_timer = 0
                self.dia_5_timer += 1

                if self.dia_5_timer == 50:
                    movie.button = 8
                    MODE_editor = 1


class Car:

    image0 = None
    image0_1 = None

    image1 = None
    image2 = None
    image3 = None
    image4 = None
    image5 = None
    image6 = None
    image7 = None
    image8 = None
    image9 = None

    def __init__(self):

        self.x0 = -1000
        self.y0 = 50
        self.image0 = load_image('Resource\Image\Main_state_3\car_1_r.png')
        self.image0_1 = load_image('Resource\Image\Main_state_3\car_3_r.png')


        self.x1 = 1000
        self.x2 = 1500
        self.x3 = 2000
        self.x4 = 3500
        self.x5 = 4000
        self.x6 = 6000
        self.x7 = 5000
        self.x8 = 4000
        self.x9 = 6000

        self.y1 = 0
        self.y2 = 0
        self.y3 = 0
        self.y4 = 0
        self.y5 = 0
        self.y6 = 0
        self.y7 = 0
        self.y8 = 0
        self.y9 = 0

        self.speed = 10

        self.image1 = load_image('Resource\Image\Main_state_3\car_1.png')
        self.image2 = load_image('Resource\Image\Main_state_3\car_3.png')
        self.image3 = load_image('Resource\Image\Main_state_3\car_2.png')
        self.image4 = load_image('Resource\Image\Main_state_3\car_4.png')
        self.image5 = load_image('Resource\Image\Main_state_3\car_3.png')
        self.image6 = load_image('Resource\Image\Main_state_3\car_2.png')
        self.image7 = load_image('Resource\Image\Main_state_3\car_1.png')
        self.image8 = load_image('Resource\Image\Main_state_3\car_4.png')
        self.image9 = load_image('Resource\Image\Main_state_3\car_1.png')


    def update(self):
        global back, movie

        if movie.button == 4:
            self.x0 += self.speed

        if movie.button >= 6:
            self.x1 -= self.speed
            self.x2 -= self.speed
            self.x3 -= self.speed
            self.x4 -= self.speed
            self.x5 -= self.speed
            self.x6 -= self.speed
            self.x7 -= self.speed
            self.x8 -= self.speed
            self.x9 -= self.speed

            self.y1 = 700 - back.map_move
            self.y2 = 900 - back.map_move
            self.y3 = 1100 - back.map_move
            self.y4 = 1300 - back.map_move
            self.y5 = 1500 - back.map_move
            self.y6 = 1900 - back.map_move
            self.y7 = 2200 - back.map_move
            self.y8 = 2300 - back.map_move
            self.y9 = 2500 - back.map_move

    def draw(self):
        global movie

        if movie.button == 4:
            self.image0.draw_to_origin(self.x0, self.y0)
            self.image0_1.draw_to_origin(self.x0 - 1500, self.y0 + 150)
            self.image0.draw_to_origin(self.x0 + 800, self.y0 + 150)

        if movie.button >= 6:
            self.image1.draw_to_origin(self.x1, self.y1)
            self.image2.draw_to_origin(self.x2, self.y2)
            self.image3.draw_to_origin(self.x3, self.y3)
            self.image3.draw_to_origin(self.x4, self.y4)
            self.image3.draw_to_origin(self.x5, self.y5)
            self.image3.draw_to_origin(self.x6, self.y6)
            self.image3.draw_to_origin(self.x7, self.y7)
            self.image3.draw_to_origin(self.x8, self.y8)
            self.image3.draw_to_origin(self.x9, self.y9)


class Effect:
    def __init__(self):
        self.effect_button = 0


class Back:
    image = None
    grid_img = None

    def __init__(self):
        self.image = load_image('Resource\Image\Main_state_3\MAP_1.png')
        self.grid_img = load_image('Resource\Image\grid.png')
        self.map_move = 0

    def draw(self):
        self.image.clip_draw_to_origin(0, self.map_move, 1280, 720, 0, 0)

    def draw_grid(self):
        if grid_button == 1:
                self.grid_img.clip_draw_to_origin(0, 0, SCREEN_X , SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)


class Son:
    image = None

    def __init__(self):
        self.x, self.y = 100, 4000  # 120
        self.speed = 0
        self.frame = 0
        self.image = load_image('Resource\Image\Main_state_3\dkemf_character_sprite.png')
        self.dir = 1
        self.frame_time = 0
        self.button_draw_son = 1


        self.y_plus = 0
        # self.frame_off = 0
        # self.timer = 0
        # self.count = 0

    def update(self):
        global back, movie

        self.y = 4070 - back.map_move + self.y_plus

        if not movie.button >= 4:
            self.x += self.dir * self.speed  # 1번의 단위시간동안 1번 이동합니다.

        if self.speed:
            self.frame_time += 1       #프레임을 결정하는 단위 시간을 올려줍니다.
        elif not self.speed:
            self.frame_time = 0       #프레임을 결정하는 단위 시간을 올려줍니다.
            self.frame = 0

        # if self.speed and self.frame_time % 8 == 0:  # 조각을 결정합니다 . 5프레임 1번씩 이미지를 변환
        if self.frame_time % 8 == 1:  # 조각을 결정합니다 . 5프레임 1번씩 이미지를 변환
            self.frame = self.frame % 6 + 1

        if movie.button == 8:
            self.frame = 0
            self.frame_time = 0

    def draw(self):
        if self.button_draw_son == 1:
            if self.dir == 1:
                self.image.clip_draw(self.frame * 80, 200, 70, 100, self.x, self.y, 35, 50)
            elif self.dir == -1:
                self.image.clip_draw(self.frame * 80, 0, 70, 100, self.x, self.y, 35, 50)


class Father:
    image = None

    def __init__(self):
        self.x, self.y = 1300, 300 # 120
        self.speed = 0
        self.frame = 0
        self.image = load_image('Resource\Image\Main_state_3\Father_character_sprite.png')
        self.dir = -1
        self.frame_time = 0
        self.button_draw_father = 1

        self.y_plus = 0
       # self.frame_off = 0
       # self.timer = 0
       # self.count = 0

    def update(self):
        global back

        self.y = 300 - back.map_move + self.y_plus

        self.x += self.dir * self.speed  # 1번의 단위시간동안 1번 이동합니다.

        if movie.button < 6:
            if self.speed:
                self.frame_time += 1       #프레임을 결정하는 단위 시간을 올려줍니다.
            elif not self.speed:
                self.frame_time = 0       #프레임을 결정하는 단위 시간을 올려줍니다.
                self.frame = 0
        elif movie.button >= 6:
            self.frame_time += 1

        # if self.speed and self.frame_time % 8 == 0:     #조각을 결정합니다 . 5프레임 1번씩 이미지를 변환
        if self.frame_time % 8 == 1:  # 조각을 결정합니다 . 5프레임 1번씩 이미지를 변환
            self.frame = self.frame % 6 + 1

        if movie.button == 8:
            self.frame = 0
            self.frame_time = 0

    def draw(self):
        if self.button_draw_father == 1:
            if self.dir == 1:
               self.image.clip_draw(self.frame * 80, 200, 70, 100, self.x, self.y)
            elif self.dir == -1:
               self.image.clip_draw(self.frame * 80, 0, 70, 100, self.x, self.y)

    def insert_key(self, events):
        global grid_button, back

        for event in events:
            if event.type == SDL_QUIT:
                game_framework.quit()
            elif event.type == SDL_KEYDOWN:
                if event.key == SDLK_LEFT:
                    self.dir = -1
                    self.speed = FATHER_SPEED
                elif event.key == SDLK_RIGHT:
                    self.dir = 1
                    self.speed = FATHER_SPEED
                elif event.key == SDLK_g:
                    if grid_button == 0:
                        grid_button = 1
                    elif grid_button == 1:
                        grid_button = 0
                elif event.key == SDLK_u:
                    back.map_move += 500
                elif event.key == SDLK_d:
                    back.map_move -= 500

            elif event.type == SDL_KEYUP:
                self.frame = 0
                self.speed = 0


def enter():
    global father, back, son, movie, car, title, dia
    father = Father()
    back = Back()
    son = Son()
    movie = Movie()
    car = Car()
    title = Title()
    dia = Dia()


def exit():
    global father, back, son, movie, car, title, dia
    del (father)
    del (son)
    del (movie)
    del (car)
    del (back)
    del (title)
    del (dia)

    #close_canvas()


def update():
    global father, son, movie, car, title, MODE_editor, dia

    if MODE_editor == 1:
        father.update()
        son.update()
        car.update()
        movie.Scene_type()
    elif MODE_editor == 0:
        title.update()
    elif MODE_editor == 2:
        dia.update()

    delay(0.02)


def draw():
    global father, son, back, car, title, MODE_editor, dia
    clear_canvas()

    if MODE_editor >= 1:
        back.draw()
        son.draw()
        father.draw()
        car.draw()
        dia.draw()
    elif MODE_editor == 0:
        title.draw()

    back.draw_grid()
    update_canvas()

def handle_events():
    global father
    events = get_events()
    father.insert_key(events)


def pause(): pass


def resume(): pass

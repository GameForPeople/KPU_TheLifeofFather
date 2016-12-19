import game_framework

from pico2d import *

# 맵! 만들고!! 또는 그냥 회사이미지로 가던가 하고!// 불투명도 이미지 통해서 op값 조정 추가하고, 대사 추가하기!!2

name = "Main_State_3"

SCREEN_X = 1280
SCREEN_Y = 720

FATHER_SPEED = 4
grid_button = 0

father = None
son = None
back = None
effect = None
movie = None


class Movie: #여기서 그냥 모든 걸 박살 내 버리자!!!암ㄴㄷ호ㅓㅏㄹ안유라ㅗㄴ아!!
    def __init__(self):
        self.button = 1

    def first_scene(self):
        global father, back

        if father.x > 620:
            father.dir = -1
            father.speed = FATHER_SPEED

        elif father.x <= 620:
            father.speed = 0
            self.button = 2

    def second_scene(self):
        global father, back

        if back.map_move < 4000:
            back.map_move += 10

        elif back.map_move >= 4000:
            self.button = 3

    def Scene_type(self):
        if self.button == 1:
            Movie.first_scene(self)
        elif self.button == 2:
            Movie.second_scene(self)



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
        self.dir = -1
        self.frame_time = 0
        self.button_draw_son = 1
        # self.frame_off = 0
        # self.timer = 0
        # self.count = 0

    def update(self):
        global back

        self.y = 1000 - back.map_move

        self.x += self.dir * self.speed  # 1번의 단위시간동안 1번 이동합니다.

        if self.speed:
            self.frame_time += 1  # 프레임을 결정하는 단위 시간을 올려줍니다.

        if self.speed and self.frame_time % 8 == 0:  # 조각을 결정합니다 . 5프레임 1번씩 이미지를 변환
            self.frame = self.frame % 6 + 1

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
       # self.frame_off = 0
       # self.timer = 0
       # self.count = 0

    def update(self):
        global back

        self.y = 300 + back.map_move

        self.x += self.dir * self.speed  # 1번의 단위시간동안 1번 이동합니다.

        if self.speed:
            self.frame_time += 1       #프레임을 결정하는 단위 시간을 올려줍니다.

        if self.speed and self.frame_time % 8 == 0:     #조각을 결정합니다 . 5프레임 1번씩 이미지를 변환
            self.frame = self.frame % 6 + 1

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
    global father, back, son, movie
    father = Father()
    back = Back()
    son = Son()
    movie = Movie()


def exit():
    pass
    #close_canvas()


def update():
    global father, son, movie
    father.update()
    son.update()
    movie.Scene_type()
    delay(0.02)


def draw():
    global father, son, back

    clear_canvas()
    back.draw()
    son.draw()
    father.draw()

    back.draw_grid()
    update_canvas()


def handle_events():
    global father
    events = get_events()
    father.insert_key(events)


def pause(): pass


def resume(): pass

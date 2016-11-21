import game_framework
import title_state

from pico2d import *


name = "StartState"

SCREEN_X = 1280
SCREEN_Y = 720

FATHER_SPEED = 3
grid_button = 0
map_sector = 1  # 2장은 가로로 볼떄 크게 두가지 페이지로 이루어집니다!! 1은 집하고 베이커리잇는곳 2는 회사잇는곳! 스크롤링은 추후처리

father = None
back = None


class Back:
    image = None
    out_image = None
    grid_img = None
    image_select = 1            # 1일때는 in! 2일때는 아웃!이미지 프린팅!

    def __init__(self):
        self.image = load_image('Resource\Image\Main_state_2\MAP_2_back.png')
        self.out_image = load_image('Resource\Image\Main_state_2\MAP_2_back_2.png')
        self.grid_img = load_image('Resource\Image\grid.png')

    def draw(self):
        global map_sector
        if self.image_select == 1:
            self.image.clip_draw_to_origin(0 + SCREEN_X * (map_sector - 1), 0, SCREEN_X, SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)
        elif self.image_select == 2:
            self.out_image.clip_draw_to_origin(0 + SCREEN_X * (map_sector - 1), 0, SCREEN_X, SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)

    def draw_front(self):
        pass

    def draw_grid(self):
        if grid_button == 1:
                self.grid_img.clip_draw_to_origin(0, 0, SCREEN_X , SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)


class Father:
    image = None

    def __init__(self):
        self.x, self.y = 470, 120 # 120
        self.speed = 0
        self.frame = 0
        self.image = load_image('Resource\Image\Main_state_2\Father_character_sprite.png')
        self.dir = -1
        self.frame_time = 0
       # self.frame_off = 0
       # self.timer = 0
       # self.count = 0

    def update(self):
        global back
        global map_sector

        self.x += self.dir * self.speed  # 1번의 단위시간동안 1번 이동합니다.

        if map_sector == 1:     # 캐릭터가 밖으로 나올경우! 집모양을 바꿔줄꺼야!
            if self.x > 520:
                back.image_select = 2

            if self.x > SCREEN_X - 30:
                map_sector = 2
                self.x = 30

        if self.speed:
            self.frame_time += 1       #프레임을 결정하는 단위 시간을 올려줍니다.

        if self.speed and self.frame_time % 5 == 0:     #조각을 결정합니다 . 5프레임 1번씩 이미지를 변환
            self.frame = self.frame % 6 + 1

    def draw(self):
        if self.dir == 1:
           self.image.clip_draw(self.frame * 80, 200, 70, 100, self.x, self.y)
        elif self.dir == -1:
           self.image.clip_draw(self.frame * 80, 0, 70, 100, self.x, self.y)

    def insert_key(self, events):
        global grid_button

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
            elif event.type == SDL_KEYUP:
                self.frame = 0
                self.speed = 0


def enter():
    global father, back
    father = Father()
    back = Back()


def exit():
    pass
    #close_canvas()


def update():
    global father
    father.update()


def draw():
    global father, back

    clear_canvas()
    back.draw()
    father.draw()

    back.draw_grid()
    update_canvas()


def handle_events():
    global father
    events = get_events()
    father.insert_key(events)


def pause(): pass


def resume(): pass

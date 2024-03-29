import game_framework

from pico2d import *

name = "Main_State_4"

SCREEN_X = 1280
SCREEN_Y = 720
FATHER_SPEED = 4

father = None
back = None
bus = None
movie = None

grid_button = 0


class Movie:
    def __init__(self):
        self.button = 1
        self.timer_1 = 0

    def update(self):
        global bus, father
        if self.button == 1:
            if bus.x >= 1280:
                father.dir = 1
                father.speed = FATHER_SPEED


class Bus:

    def __init__(self):
        self.x = -300
        self.y = 180
        self.timer = 0
        self.speed = 6

        self.image_type = 0

        self.image_out = load_image('Resource\Image\Main_state\BUS_3.png')
        self.image_in = load_image('Resource\Image\Main_state\BUS_4.png')

    def draw(self):
        if self.image_type == 0:
            self.image_in.draw(self.x, self.y, 372, 230)
        elif self.image_type == 1:
            self.image_out.draw(self.x, self.y, 372, 230)

    def update(self):
        global father

        if father.button_draw_father == 0:
            if self.x < 130:
                self.x += 5
            elif self.x < 160:
                self.x += 4
            elif self.x < 200:
                self.x += 3
            elif self.x < 220:
                self.x += 2
            elif self.x < 240:
                self.x += 1
            elif self.x <= 250:

                self.timer += 1

                if self.timer == 20:
                    self.timer = 0
                    self.image_type = 1
                    father.button_draw_father = 1

        elif father.button_draw_father == 1:
            self.timer += 1

            self.x += (int)(self.timer / 10)


class Back:
    image = None
    grid_img = None

    nos_img_1 = None
    nos_img_2 = None

    black_screen = None
    light_img = None

    end_img = None

    def __init__(self):
        self.image = load_image('Resource\Image\Main_state_4\MAP_1.png')

        self.nos_img_1 = load_image('Resource\Image\Main_state_4\save_img_1_alpha.png')
        self.nos_img_2 = load_image('Resource\Image\Main_state_4\save_img_2_alpha.png')

        self.black_screen = load_image('Resource\Image\Main_state_4\_black_screen_10.png')

        self.light_img = load_image('Resource\Image\Main_state_4\Light_1.png')

        self.end_img = load_image('Resource\Image\Main_state_4\_theEnd.png')

        self.nos_1_timer = 0
        self.nos_2_timer = 0
        self.all_timer = 0
        self.black_timer = 0
        self.light_timer = 0

        self.black_button = 0
        self.light_button = 0
        self.end_button = 0

        self.mapmove = 0

        self.grid_img = load_image('Resource\Image\grid.png')

    def draw(self):
        global father
        self.image.clip_draw_to_origin(4000 + self.mapmove, 0, SCREEN_X, SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)

        for i in range(0, self.nos_1_timer, 1):
            self.nos_img_1.clip_draw_to_origin(0, 0, 703, 695, 170, 300, 300, 300)

        for i in range(0, self.nos_2_timer, 1):
            self.nos_img_2.clip_draw_to_origin(0, 0, 826, 817, 810, 300, 300, 300)

        for i in range(0, self.black_timer, 1):
            self.black_screen.draw(640, 360)

        for i in range(0, self.light_timer, 1):
            self.light_img.clip_draw_to_origin(0, 0, 262, 291, 460, 70, 262, 291)

        if self.end_button == 1:
            self.end_img.clip_draw_to_origin(0, 0, 300, 83, 490, 100, 200, 55)

    def update(self):
        global father

        if father.view_button == 1:
            self.mapmove += father.dir * father.speed


        elif father.view_button == 2:
            self.all_timer += 1

            if self.black_button == 0:
                if self.nos_1_timer < 20:
                    if self.all_timer == 3:
                        self.nos_1_timer += 1
                        self.all_timer = 0
                elif self.nos_2_timer < 20:
                    if self.all_timer == 3:
                        self.nos_2_timer += 1
                        self.all_timer = 0

                        if self.nos_2_timer == 20:
                            self.black_button = 1
                            self.all_timer = - 50

            elif self.light_button == 1:
                if self.light_timer <= 3:
                    if self.all_timer == 5:
                        self.light_timer += 1
                        self.all_timer = 0

                elif self.light_timer == 4 and self.all_timer == 20:
                    self.end_button = 1

            elif self.black_button == 1:
                if self.all_timer == 5:
                    self.nos_1_timer -= 4
                    self.nos_2_timer -= 4
                    self.black_timer += 1
                    self.all_timer = 0

                    if self.black_timer == 10:
                        self.light_button = 1

    def draw_front(self):
        pass

    def draw_grid(self):
        if grid_button == 1:
                self.grid_img.clip_draw_to_origin(0, 0, SCREEN_X , SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)


class Father:
    image = None

    def __init__(self):
        self.x, self.y = 200, 120 # 120
        self.speed = 0
        self.frame = 0
        self.image = load_image('Resource\Image\Main_state_4\youngFather_character_sprite.png')
        self.dir = 1
        self.frame_time = 0
        self.button_draw_father = 0
        self.view_button = 0

    def update(self):
        global back, FATHER_SPEED

        if self.view_button < 2:
            self.x += self.dir * self.speed  # 1번의 단위시간동안 1번 이동합니다.

            if self.speed:
                self.frame_time += 1       #프레임을 결정하는 단위 시간을 올려줍니다.

            if self.speed and self.frame_time % 5 == 0:     #조각을 결정합니다 . 5프레임 1번씩 이미지를 변환
                self.frame = self.frame % 6 + 1

        if self.view_button == 0:
            if self.x > 640:
                self.x = 640
                self.view_button = 1
                FATHER_SPEED = 2
                self.speed = 2

        elif self.view_button == 1:
            if back.mapmove > 700:
                self.view_button = 2
                self.button_draw_father = 0

    def draw(self):
        if self.button_draw_father == 1:
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
    global father, back, bus, movie
    father = Father()
    back = Back()
    bus = Bus()
    movie = Movie()


def exit():
    global movie, bus, back, father
    del (movie)
    del (bus)
    del (back)
    del (father)

    #close_canvas()


def update():
    global father, bus, back, movie
    father.update()
    bus.update()
    back.update()
    movie.update()

    delay(0.02)


def draw():
    global father, back, bus

    clear_canvas()
    back.draw()
    father.draw()
    bus.draw()

    back.draw_grid()
    update_canvas()


def handle_events():
    global father
    events = get_events()
    father.insert_key(events)


def pause(): pass


def resume(): pass

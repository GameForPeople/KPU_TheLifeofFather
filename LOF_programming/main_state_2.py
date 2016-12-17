import game_framework

from pico2d import *

# 맵! 만들고!! 또는 그냥 회사이미지로 가던가 하고!// 불투명도 이미지 통해서 op값 조정 추가하고, 대사 추가하기!!2

name = "Main_State_2"

SCREEN_X = 1280
SCREEN_Y = 720


FATHER_SPEED = 10
grid_button = 0
map_sector = 1  # 2장은 가로로 볼떄 크게 두가지 페이지로 이루어집니다!! 1은 집하고 베이커리잇는곳 2는 회사잇는곳! 스크롤링은 추후처리

father = None
back = None
effect = None


class Effect:  # 각종 이펙트를 클래스 내부에서 정의할껍니다! 이펙트란 한놈의 여러 성질이니까.

    sun_img = None
    moon_img = None

    white_img = None
    black_img = None

    zoom_img = None             # 이미지 크기 변환하기 -> 쫌 이상함

    def __init__(self):
        self.button_camera_effect = 0
        self.button_weather_effect = 0

        self.camera_effect_value = 0
        self.weather_effect_value = 0

        self.sun_img = load_image('Resource\Image\Main_state_2\sun_img.png')
        self.sun_x = 640 * math.cos(3.14)
        self.sun_y = 640 * math.sin(3.14)
        self.sun_timer = 0.50
        self.sun_button = 1

        self.moon_img = load_image('Resource\Image\Main_state_2\moon_img.png')
        self.moon_x = 640 * math.cos(3.14)
        self.moon_y = 640 * math.sin(3.14)
        self.moon_timer = 0.50
        self.moon_button = 0

        self.white_img = load_image('Resource\Image\Main_state_2\white_effect.png')
        self.white_timer = 0
        self.white_draw_count = 0
        self.black_img = load_image('Resource\Image\Main_state_2\_black_effect.png')
        self.black_timer = 0
        self.black_draw_count = 0

        self.zoom_img = load_image('Resource\Image\Main_state_2\save_img.png')
        self.zoom_button = 0
        self.zoom_value = 0

    def zoom_effect_update(self):
        global map_sector
        global father, back

        if self.zoom_button == 1:
            self.zoom_value += 1

            print(self.zoom_value)

            if self.zoom_value == 45:
                self.zoom_button = 0
                self.camera_effect_value = 0

                self.moon_button = 2

                map_sector = 2
                back.image_select = 3

                father.x = 550
                father.button_draw_father = 1


    def zoom_effect_draw(self):
        if self.zoom_button == 1:
            self.zoom_img.clip_draw_to_origin(0 + (int)(490 / 40) * self.zoom_value, 0 + (int)(180 / 40) * self.zoom_value,
                                              1280 - (int)(1100 / 40) * self.zoom_value, 720 - (int)(560/40) *self.zoom_value , 0, 0, 1280, 720)

    def weather_effect_update(self):

        if self.button_weather_effect == 1:
            if self.sun_button == 1:
                self.sun_timer -= 0.01

                self.sun_x = 640 + 640 * math.cos(3.14 + self.sun_timer)
                self.sun_y = 640 * math.sin(3.14 + self.sun_timer)

                if self.sun_x < 640:
                    self.white_timer += 1
                    if self.white_timer == 4:
                        self.white_timer = 0
                        self.white_draw_count += 1
                elif self.sun_x > 640:
                    self.white_timer += 1
                    if self.white_timer == 4:
                        self.white_timer = 0
                        self.white_draw_count -= 1
                    if self.sun_y < - 100:
                        self.sun_button = 0
                        self.moon_button = 1

            elif self.moon_button == 1:
                self.moon_timer -= 0.01

                # print(self.moon_timer)
                self.moon_y = 640 * math.sin(3.14 + self.moon_timer)
                self.moon_x = 640 + 640 * math.cos(3.14 + self.moon_timer)

                if self.moon_x < 640:
                    self.black_timer += 1
                    if self.black_timer == 4:
                        self.black_timer = 0
                        self.black_draw_count += 1
                else:
                    # self.black_timer += 1
                    #if self.black_timer == 4:
                    #    self.black_timer = 0
                    #    self.black_draw_count -= 1
                    #if self.moon_y < - 100:
                        self.moon_button = 2
                        self.zoom_button = 1

    def weather_effect_draw(self):
        if self.sun_button == 1:
            self.sun_img.draw(self.sun_x, self.sun_y)

            for i in range (0, self.white_draw_count, 1):
                self.white_img.draw(640, 360)
        elif self.moon_button >= 1:
            if self.moon_button == 1:
                self.moon_img.draw(self.moon_x, self.moon_y)

            if self.moon_button >= 1:
                for i in range (0, self.black_draw_count, 1):
                    self.black_img.draw(640, 360)

    def camera_effect(self):

        if self.button_camera_effect == 1:
            self.camera_effect_value += 10
            print(self.camera_effect_value)

            if self.camera_effect_value > 1550:
                self.button_camera_effect = 0
                self.button_weather_effect = 1


class Back:
    image = None
    out_image = None
    dark_out_image = None
    grid_img = None
    image_select = 1            # 1일때는 in! 2일때는 아웃!이미지 프린팅!
    Map_Move = 1280

    def __init__(self):
        self.image = load_image('Resource\Image\Main_state_2\MAP_2_back.png')
        self.out_image = load_image('Resource\Image\Main_state_2\MAP_2_back_2.png')
        self.dark_out_image = load_image('Resource\Image\Main_state_2\MAP_2_back_3.png')

        self.grid_img = load_image('Resource\Image\grid.png')

    def draw(self):
        global map_sector, effect
        if self.image_select == 1:
            self.image.clip_draw_to_origin(0 + SCREEN_X * (map_sector - 1), 0 + effect.camera_effect_value, SCREEN_X,
                                           SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)
        elif self.image_select == 2:
            self.out_image.clip_draw_to_origin(0 + SCREEN_X * (map_sector - 1), 0 + effect.camera_effect_value, SCREEN_X,
                                               SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)
        elif self.image_select == 3:
            self.dark_out_image.clip_draw_to_origin(0 + self.Map_Move , 0,
                                                    SCREEN_X + self.Map_Move, SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)

    def update_mapmove(self):
        global father

        if self.image_select == 3:
            self.Map_Move += father.dir * father.speed

    def draw_front(self):
        pass

    def draw_grid(self):
        if grid_button == 1:
                self.grid_img.clip_draw_to_origin(0, 0, SCREEN_X , SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)

class Father:
    image = None

    def __init__(self):
        self.x, self.y = 100, 120 # 120
        self.speed = 0
        self.frame = 0
        self.image = load_image('Resource\Image\Main_state_2\Father_character_sprite.png')
        self.dir = -1
        self.frame_time = 0
        self.button_draw_father = 1
        self.need_effect = 0
       # self.frame_off = 0
       # self.timer = 0
       # self.count = 0

    def update(self):
        global back
        global map_sector
        global effect

        self.x += self.dir * self.speed  # 1번의 단위시간동안 1번 이동합니다.

        if map_sector == 1:     # 캐릭터가 밖으로 나올경우! 집모양을 바꿔줄꺼야!
            if self.x > 520:
                back.image_select = 2

            if self.x > SCREEN_X - 30:
                map_sector = 2
                self.x = 30

        elif map_sector == 2:
            if self.need_effect == 0 and self.x > 520 and self.speed == 0 and self.x < 600:  # 캐릭터가 회사건물에 들어갈떄...
                self.button_draw_father = 0             #아빠의 위치를 off해주고
                effect.button_camera_effect = 1                #카메라 이펙트 1 작동!
                self.x = 0                              #위치를 바꿔줘서 렉을 방지할꺼야!
                self.need_effect = 1                    # 무한루프를 방지할꺼야!


        if self.speed:
            self.frame_time += 1       #프레임을 결정하는 단위 시간을 올려줍니다.

        if self.speed and self.frame_time % 5 == 0:     #조각을 결정합니다 . 5프레임 1번씩 이미지를 변환
            self.frame = self.frame % 6 + 1

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
    global father, back, effect
    father = Father()
    back = Back()
    effect = Effect()


def exit():
    pass
    # close_canvas()


def update():
    global father
    father.update()
    effect.camera_effect()
    effect.weather_effect_update()
    effect.zoom_effect_update()
    back.update_mapmove()

    delay(0.02)


def draw():
    global father, back, effect

    clear_canvas()
    back.draw()
    father.draw()
    effect.weather_effect_draw()
    effect.zoom_effect_draw()

    back.draw_grid()
    update_canvas()


def handle_events():
    global father
    events = get_events()
    father.insert_key(events)


def pause(): pass


def resume(): pass

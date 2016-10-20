import game_framework
import main_state
from pico2d import *


name = "TitleState"
image = None
bgm = None
image_10 = None
image_1 = None

draw_count = 0
draw_dir = 1
num_10 = 0
num_1 = 0

def enter():
    global image, bgm, image_1, image_10

    image = load_image('black_screen.png')
    image_10 = load_image("story_1_10.png")
    image_1 = load_image("story_1_1.png")
    bgm = Music('Main_BGM.wav')

    #bgm.play()

def exit():
    global image
    del(image)
    pass

def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)

def draw():

    global num_10, num_1, draw_count, draw_dir
    clear_canvas()

    image.draw(640, 360)

    if draw_count >= 0:

        num_10 = (int)(draw_count / 10)     #설정하려는 불투명도의 10의 자리값
        num_1 = (int)(draw_count % 10)      #설정하려는 불투명도의 1의 자리값

        for i in range(0, num_10, 1):
            image_10.draw(640,360)          #불투명도 10짜리의 그림을 몇번 num_10번 그립니다.

        for i in range(0 , num_1, 1):
            image_1.draw(640,360)           #불투명도 1짜리의 그림을 몇번 num_1번 그립니다.

        draw_count = draw_count + draw_dir  #draw_dir은 두 개의 값을 가집니다. -> 밝아졌다가 어두워졋다가! 즉 +1 -> -1

        if draw_count == 130:               #가장 밝은 상태는 100번 까지며 그 이후의 값은 영향이 없으나 가장 밝을떄의 값을 오래지속하도록
            draw_dir = -1                   #어두워져라 얍!

    update_canvas()
    pass

def update():
    pass

def pause():
    pass

def resume():
    pass







import game_framework
import main_state
from pico2d import *

name = "TitleState"
image = None
back_1 = None
image_10 = None
image_1 = None
first_screen = None
chapter_1 = None
chapter_10 = None

turn_check = 1
draw_count = 0
draw_dir = 1

draw_count_chapter = 0
draw_dir_chapter = 1

num_10 = 0
num_1 = 0

num_10_chapter = 0
num_1_chapter = 0

black_count = 50
black_1_count = 100

buffer_timer = 0

def enter():
    global image, bgm, image_1, image_10, back_1, first_screen, chapter_1, chapter_10

    chapter_1 = load_image('Resource\Image\Title_state\chapter_1_1.png')
    chapter_10 = load_image('Resource\Image\Title_state\chapter_1_10.png')

    image = load_image('Resource\Image\Title_state\_black_screen_10.png')
    back_1 = load_image('Resource\Image\Title_state\_black_screen_1.png')
    image_10 = load_image("Resource\Image\Title_state\story_1_10.png")
    image_1 = load_image("Resource\Image\Title_state\story_1_1.png")
    first_screen = load_image("Resource\Image\Title_state\First_screen.png")

def exit():
    global image, back_1, image_10, image_1, first_screen, chapter_1, chapter_10

    del(image)
    del(back_1)
    del(image_10)
    del(image_1)
    del(first_screen)
    del(chapter_1)
    del(chapter_10)


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                pass
def draw():

    global num_10, num_1, draw_count, draw_dir, black_count, back_1, first_screen, num_10_chapter, num_1_chapter, \
        draw_count_chapter, draw_dir_chapter, turn_check, chapter_1, chapter_10

    clear_canvas()

    first_screen.draw(640, 360)             # 사기치는 이미지!!!

    for i in range(0, black_count, 1):
        image.draw(640, 360)

    if turn_check == 1:
        if draw_count_chapter >= 0:

            num_10_chapter = (int)(draw_count_chapter / 10)  # 설정하려는 불투명도의 10의 자리값
            num_1_chapter = (int)(draw_count_chapter % 10)  # 설정하려는 불투명도의 1의 자리값

            for i in range(0, num_10_chapter, 1):
                chapter_10.draw(640, 360)  # 불투명도 10짜리의 그림을 몇번 num_10번 그립니다.

            for i in range(0, num_1_chapter, 1):
                chapter_1.draw(640, 360)  # 불투명도 1짜리의 그림을 몇번 num_1번 그립니다.

            draw_count_chapter = draw_count_chapter + draw_dir_chapter  # draw_dir은 두 개의 값을 가집니다. -> 밝아졌다가 어두워졋다가! 즉 +1 -> -1

            if draw_count_chapter == 130:  # 가장 밝은 상태는 100번 까지며 그 이후의 값은 영향이 없으나 가장 밝을떄의 값을 오래지속하도록
                draw_dir_chapter = -1  # 어두워져라 얍!

            if draw_count_chapter == 0:
                turn_check = 2

    elif turn_check == 3:
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

def update():
    global draw_dir, draw_count, black_count, turn_check, buffer_timer

    if turn_check == 1:
        pass
    elif turn_check == 2:
        buffer_timer += 1

        if buffer_timer == 50:
            turn_check = 3

    elif turn_check == 3:
        if draw_dir == -1 and draw_count < 100 and draw_count % 2 == 1:
            black_count -= 1

        if draw_dir == -1 and draw_count == 0:
            game_framework.change_state(main_state)

def pause():
    pass

def resume():
    pass







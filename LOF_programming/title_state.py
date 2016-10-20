import game_framework
import main_state
from pico2d import *

name = "TitleState"
image = None
bgm = None
image_10 = None
image_1 = None


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
    clear_canvas()

    image.draw(640, 360)

    update_canvas()
    pass

def update():
    pass

def pause():
    pass

def resume():
    pass







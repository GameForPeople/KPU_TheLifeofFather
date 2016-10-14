import game_framework
import title_state

from pico2d import *


name = "StartState"
image = None
logo_time = 0.0
onoff_push = 0
#alpha_value = 0

SCREEN_X = 1280
SCREEN_Y = 720

def enter():
    global image
    open_canvas()
    image = load_image('WarpLogo.png')
    #image_1 = load_image()
    #image.opacify(0)


def exit():
    global image
    del (image)
    close_canvas()


def update():
    global logo_time
    global onoff_push
    #global alpha_value

    #alpha_value = alpha_value + 10

    if (logo_time > 0.5):
        logo_time = 0
        # game_framework.quit()
        game_framework.push_state(title_state)
        onoff_push = 1

    if (onoff_push != 1):
        delay(0.01)
        logo_time += 0.01

def draw():
    global image
   # global alpha_value

    clear_canvas()

    image.clip_draw_to_origin(0, 0 , 600, 300, 0, 0, SCREEN_X, SCREEN_Y )
    #image.opacify(100)

    update_canvas()


def handle_events():
    events = get_events()
    pass


def pause(): pass


def resume(): pass





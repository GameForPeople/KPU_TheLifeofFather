import game_framework
import title_state

from pico2d import *


name = "StartState"
image = None
image2 = None
logo_time = 0.0
image_change = 0
#alpha_value = 0

SCREEN_X = 1280
SCREEN_Y = 720

def enter():
    global image, image2
    open_canvas()
    image = load_image('WarpLogo.png')
    image2 = load_image('DESIGNEDBY.png')
    #image_1 = load_image()
    #image.opacify(0)


def exit():
    global image
    del (image)
    close_canvas()


def update():
    global logo_time
    global image_change
    #global alpha_value

    #alpha_value = alpha_value + 10

    if (logo_time > 1.0):
        logo_time = 0
        # game_framework.quit()
        image_change = image_change + 1

    if image_change < 2:
        delay(0.01)
        logo_time += 0.01

    if image_change == 2:
        game_framework.push_state(title_state)
def draw():
    global image, image2, image_change
   # global alpha_value

    clear_canvas()

    if image_change == 0:
        image.clip_draw_to_origin(0, 0 , 600, 300, 0, 0, SCREEN_X, SCREEN_Y )
    if image_change == 1:
        image2.clip_draw_to_origin(0, 0, SCREEN_X, SCREEN_Y, 0, 0, SCREEN_X, SCREEN_Y)
    #image.opacify(100)

    update_canvas()


def handle_events():
    events = get_events()
    pass


def pause(): pass


def resume(): pass





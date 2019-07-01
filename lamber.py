#!/usr/bin/python3
# Print RGB color values of screen pixel at location x, y
from gi.repository import Gdk
import sys
import keyboard
import time
from Xlib import display
import numpy as np
from numba import jit


sky_color = np.array([209, 247, 255])
tree_color = np.array([158, 123, 43])

left_bound = 965
right_bound = 1024

lowset_tree = 725
middle_tree = 677
upper_tree = 625


def pixel_at(x, y, w, h):
    wi = Gdk.get_default_root_window()
    pb = Gdk.pixbuf_get_from_window(wi, x, y, w, h)

    colors = tuple(pb.get_pixels())
    pixels = [(colors[i], colors[i + 1], colors[i + 2]) for i in range(0, len(colors)//3*3, 3)]

    return pixels


@jit
def is_tree_color(color):
    current_color = np.array(list(color))

    # sky_dist = np.linalg.norm(current_color - sky_color)
    tree_dist = np.linalg.norm(current_color - tree_color)


    return tree_dist < 30


def press_left():
    from pykeyboard import PyKeyboard
    k = PyKeyboard()
    k.tap_key(k.left_key)
    # keyboard.press_and_release('left arrow')


def press_right():
    from pykeyboard import PyKeyboard
    k = PyKeyboard()
    k.tap_key(k.right_key)
    # keyboard.press_and_release('right arrow')


def press(where):
    if where == 'left':
        press_left()
    if where == 'right':
        press_right()


def double_press(where):
    global current_position

    press(where)
    time.sleep(0.01)
    press(where)

    current_position = where


def is_tree_up(where):
    HEIGHT = 135
    WIDTH = 10

    start_y = middle_tree - HEIGHT + 5

    if where == 'left':
        start_x = left_bound - 20
    else:
        start_x = right_bound + 5


    pixels = pixel_at(start_x, start_y, WIDTH, HEIGHT)
    trees = [is_tree_color(pix) for pix in pixels]

    print('upper', where, sum(trees))

    return sum(trees)


def is_tree_near(where):
    HEIGHT = 55
    WIDTH = 5

    start_y = lowset_tree + 5 - HEIGHT

    if where == 'left':
        start_x = left_bound - 50
    else:
        start_x = right_bound + 10


    pixels = pixel_at(start_x, start_y, WIDTH, HEIGHT)
    trees = [is_tree_color(pix) for pix in pixels]

    print('near', where, sum(trees))

    return sum(trees)


def lost():
    pixels = pixel_at(992, 709, 5, 5)
    trees = [is_tree_color(pix) for pix in pixels]

    return sum(trees) <= 5


def should_go_left():
    global current_position

    # if current_position == 'right' and is_tree_near('left') > 7:  # слева дерево рядом
    #     return False  # точно не идем туда
    #
    # if current_position == 'left' and is_tree_near('right') > 7: # справа дерево рядом
    #     return True  # Точно идем влево
    l, r = is_tree_up('left'), is_tree_up('right')

    if l > r:  # слева дерево сверху
        return False

    if l == r:
        return current_position == 'left'

    return True


# need xhost + to launch
# while True:
   # data = display.Display().screen().root.query_pointer()._data
   # x, y = data["root_x"], data["root_y"]
   # pix = pixel_at(x, y, 1, 1)
   #
   # print(x, y, pix)
   # time.sleep(0.2)



current_position = 'right'

while True:

    if lost():
        print('Проиграл')
        time.sleep(0.5)
        continue

    if should_go_left():
        print('Жмем <-')
        double_press('left')
    else:
        print('Жмем ->')
        double_press('right')

    # elif not l_tree and not r_tree:
    #     print('NO TREES')
    #     press_left()

    time.sleep(0.11)
    print('-'*60)


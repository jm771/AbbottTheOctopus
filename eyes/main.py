from time import sleep
import os
import sys

from eye_controllers import make_left_eye_display, make_right_eye_display
from eyes.animations.excited import ExcitedAnimation
from animations.moving_eyes import IdleEyesAnimation

left_display = make_left_eye_display()
right_display = make_right_eye_display()

idle_animation = IdleEyesAnimation(left_display.width, left_display.height)
excited_animation = ExcitedAnimation(left_display.width, left_display.height)

def play_animation(animation):
    assert animation.length is not None, f"animation has no length - can't be played one time"
    for i in range (0, animation.length):
        animation.display_frame(left_display, right_display, i)
        sleep(0.1)
    animation.reset()

def select_animation(character):
    if character == 'e':
        return excited_animation

    return None

i = 0
while True:
    animation = select_animation(os.read(sys.stdin.fileno(), 1))

    if animation is not None:
        idle_animation.reset()
        i = 0
        play_animation(animation)

    idle_animation.display_frame(left_display, right_display, i)
    i+=1
    sleep(0.1)
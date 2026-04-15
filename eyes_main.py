from time import sleep
import sys
import select


from eye_controllers import make_left_eye_display, make_right_eye_display
from animations.excited import ExcitedAnimation
from animations.moving_eyes import IdleEyesAnimation
from animations.heart import HeartAnimation

left_display = make_left_eye_display()
right_display = make_right_eye_display()

idle_animation = IdleEyesAnimation()
excited_animation = ExcitedAnimation()
heart_animation = HeartAnimation()


def play_animation(animation):
    assert (
        animation.length() is not None
    ), f"animation has no length - can't be played one time"
    for i in range(0, animation.length()):
        animation.display_frame(left_display, right_display, i)
        sleep(0.1)
    animation.reset()


def select_animation(character):
    if character == "e":
        return excited_animation
    if character == "h":
        return heart_animation

    return None


def readline_nonblocking():
    if select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.readline().rstrip()

    return None


i = 0
while True:
    animation = select_animation(readline_nonblocking())

    if animation is not None:
        idle_animation.reset()
        i = 0
        play_animation(animation)

    idle_animation.display_frame(left_display, right_display, i)
    i += 1
    sleep(0.1)

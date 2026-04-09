from time import sleep

from eye_controllers import make_left_eye_display, make_right_eye_display
from moving_eyes import IdleEyesAnimation

left_display = make_left_eye_display()
right_display = make_right_eye_display()

idle_animation = IdleEyesAnimation(left_display.width, left_display.height)

i = 0
while True:
    idle_animation.display_frame(left_display, right_display, i)
    i+=1
    sleep(0.1)
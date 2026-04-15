import time
from eyes.eye_controllers import make_left_eye_display, make_right_eye_display
from adafruit_rgb_display import color565

display1 = make_left_eye_display()
display2 = make_right_eye_display()

# Main loop:
while True:
    # Clear the display
    display1.fill(0)
    display2.fill(0)
    # Draw a red pixel in the center.
    display1.pixel(120, 160, color565(255, 0, 0))
    display2.pixel(120, 160, color565(255, 0, 0))
    # Pause 2 seconds.
    time.sleep(2)
    # Clear the screen blue.
    display1.fill(color565(0, 0, 255))
    display2.fill(color565(0, 0, 255))
    # Draw a red pixel in the center.
    display1.pixel(120, 160, color565(255, 0, 0))
    display2.pixel(120, 160, color565(255, 0, 0))
    # Pause 2 seconds.
    time.sleep(2)

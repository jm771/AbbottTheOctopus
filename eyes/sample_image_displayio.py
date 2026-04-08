
import time
from eye_controllers_displayio import make_left_eye_display, make_right_eye_display
from adafruit_rgb_display import color565

# Import adafruit image management library
import displayio
import adafruit_imageload

display1 = make_left_eye_display()
display2 = make_right_eye_display()

# # Is this a reset command?
displayio.release_displays()

# Create display group
blinka_group = displayio.Group()
bitmap, palette = adafruit_imageload.load("blinka_round.bmp",
                                           bitmap=displayio.Bitmap,
                                           palette=displayio.Palette)

grid = displayio.TileGrid(bitmap, pixel_shader=palette)
blinka_group.append(grid)

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
    display1.root_group = blinka_group
    display2.root_group = blinka_group
    time.sleep(2)



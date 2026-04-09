
import time
from eye_controllers import make_left_eye_display, make_right_eye_display
from PIL import Image

display1 = make_left_eye_display()
display2 = make_right_eye_display()

width = display1.width
height = display1.height

image1 = Image.open("Eye.png")
image_ratio = image1.width / image1.height
screen_ratio = width / height
scaled_width = width
scaled_height = image1.height * width // image1.width
image1 = image1.resize((scaled_width, scaled_height), Image.BICUBIC)
x = scaled_width // 2 - width // 2
y = scaled_height // 2 - height // 2
image1 = image1.crop((x, y, x + width, y + height))

i = 0

while True:
    im = image1.rotate(0, translate=[i, 0], fillcolor=0xffffff) 
    display1.image(im)
    display2.image(im)
    time.sleep(0.1)
    i+=1



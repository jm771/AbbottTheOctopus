
import time
from eye_controllers import make_left_eye_display, make_right_eye_display
from PIL import Image

display1 = make_left_eye_display()
display2 = make_right_eye_display()

width = display1.width
height = display1.height

image1 = Image.open("sad_kitty.png")
image_ratio = image1.width / image1.height
screen_ratio = width / height
scaled_width = width
scaled_height = image1.height * width // image1.width
image1 = image1.resize((scaled_width, scaled_height), Image.BICUBIC)
x = scaled_width // 2 - width // 2
y = scaled_height // 2 - height // 2
image1 = image1.crop((x, y, x + width, y + height))

image2 = Image.open("blinka_round.jpg")
image_ratio = image2.width / image2.height
screen_ratio = width / height
scaled_width = width
scaled_height = image2.height * width // image2.width
image2 = image2.resize((scaled_width, scaled_height), Image.BICUBIC)
x = scaled_width // 2 - width // 2
y = scaled_height // 2 - height // 2
image2 = image2.crop((x, y, x + width, y + height))

while True:
    display1.image(image1)
    display2.image(image1)
    time.sleep(2)
    display1.image(image2)
    display2.image(image2)
    time.sleep(2)



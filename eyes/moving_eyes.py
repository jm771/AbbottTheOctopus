
import time
from eye_controllers import make_left_eye_display, make_right_eye_display
from PIL import Image
import random
import math

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

currentX = 0
currentY = 0
targetX = 60
targetY = 60
speed = 10


while True:
    if random.randint() % 100 == 0:
        targetX = random.randint(-60, 60)
        targetY = random.randint(-60, 60)
        speed = random.randint(1, 10)

    if abs(currentX - targetX) <= speed:
        currentX = targetX
    else:
        currentX += math.copysign(speed, targetX - currentX)
    if abs(currentY - targetY) <= speed:
        currentY = targetY
    else:
        currentY += math.copysign(speed, targetY - currentY)


    im = image1.rotate(0, translate=[currentX, currentY], fillcolor=0xffffff) 
    display1.image(im)
    display2.image(im)
    time.sleep(0.1)



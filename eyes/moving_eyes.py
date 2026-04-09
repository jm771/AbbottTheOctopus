
import time
from typing import Optional
from PIL import Image
import random
import math
from animation import Animation

class IdleEyesAnimation(Animation):
    def __init__(self, displayWidth, displayHeight):
        self.currentX = 0
        self.currentY = 0
        self.targetX = 0
        self.targetY = 0
        self.speed = 0
        self.sustain = 3

        width = displayWidth
        height = displayHeight

        image1 = Image.open("Eye.png")
        scaled_width = width
        scaled_height = image1.height * width // image1.width
        image1 = image1.resize((scaled_width, scaled_height), Image.BICUBIC)
        x = scaled_width // 2 - width // 2
        y = scaled_height // 2 - height // 2
        self.baseImage = image1.crop((x, y, x + width, y + height))

    def reset(self):
        self.currentX = 0
        self.currentY = 0
        self.targetX = 0
        self.targetY = 0
        self.speed = 0
        self.sustain = 3

    # Animation length in frames, None -> infinite
    def length(self) -> Optional[int]:
        return None

    def display_frame(self, left_eye, right_eye, frame_number):
        self.sustain -= 1
        if self.sustain == 0:
            self.targetX = random.randint(-50, 50)
            self.targetY = random.randint(-50, 50)
            self.speed = random.randint(1, 10)
            self.sustain = random.randint(2, 20)

        if abs(self.currentX - self.targetX) <= self.speed:
            self.currentX = self.targetX
        else:
            self.currentX += math.copysign(self.speed, self.targetX - self.currentX)
        if abs(self.currentY - self.targetY) <= self.speed:
            self.currentY = self.targetY
        else:
            self.currentY += math.copysign(self.speed, self.targetY - self.currentY)


        im = self.baseImage.rotate(0, translate=[self.currentX, self.currentY], fillcolor=0xffffff) 
        left_eye.image(im)
        right_eye.image(im)
  



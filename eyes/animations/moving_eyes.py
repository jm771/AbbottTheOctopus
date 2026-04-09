
from typing import Optional
import random
import math
from animations.animation import Animation
from animations.eye_image import load_and_scale_eye_image
from display import DISPLAY_WIDTH, DISPLAY_HEIGHT

class IdleEyesAnimation(Animation):
    def __init__(self):
        self.reset()
        self.baseImage = load_and_scale_eye_image(DISPLAY_WIDTH, DISPLAY_HEIGHT)


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
  
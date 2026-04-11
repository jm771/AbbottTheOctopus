
from typing import Optional
import random
import math
from eyes.animations.animation import EyeAnimation
from eyes.animations.eye_image import load_and_scale_eye_image
from display import DISPLAY_WIDTH, DISPLAY_HEIGHT

class IdleEyesAnimation(EyeAnimation):
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
        self.lastFrame = 0

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

        # Orignal animation written for 10hz
        frames_passed = frame_number - self.lastFrame
        self.lastFrame = frame_number
        adjusted_speed = (frames_passed * self.speed) // 6

        # This setup only actually allows movement in 8 directions rather than moving directly to target
        # but looks good enough for now
        if abs(self.currentX - self.targetX) <= adjusted_speed:
            self.currentX = self.targetX
        else:
            self.currentX += math.copysign(adjusted_speed, self.targetX - self.currentX)
        if abs(self.currentY - self.targetY) <= adjusted_speed:
            self.currentY = self.targetY
        else:
            self.currentY += math.copysign(adjusted_speed, self.targetY - self.currentY)


        im = self.baseImage.rotate(0, translate=[self.currentX, self.currentY], fillcolor=0xffffff) 
        left_eye.image(im)
        right_eye.image(im)
  
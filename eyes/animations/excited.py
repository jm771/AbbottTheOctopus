
from typing import Optional
from animations.animation import Animation
from animations.eye_image import load_and_scale_eye_image
from display import DISPLAY_WIDTH, DISPLAY_HEIGHT

class ExcitedAnimation(Animation):
    def __init__(self):
        self.baseImage = load_and_scale_eye_image(DISPLAY_WIDTH, DISPLAY_HEIGHT)

    def reset(self):
        pass

    # Animation length in frames, None -> infinite
    def length(self) -> Optional[int]:
        return 15

    def display_frame(self, left_eye, right_eye, frame_number):
        OFFSET_Y = -40
        offset_x = -20 if frame_number % 2 == 0 else 20

        im = self.baseImage.rotate(0, translate=[offset_x, OFFSET_Y], fillcolor=0xffffff) 
        left_eye.image(im)
        right_eye.image(im)
  

from typing import Optional
from eyes.animations.animation import EyeAnimation
from eyes.animations.eye_image import load_and_scale_eye_image
from eyes.display import DISPLAY_WIDTH, DISPLAY_HEIGHT


class ExcitedAnimation(EyeAnimation):
    def __init__(self):
        self.baseImage = load_and_scale_eye_image(DISPLAY_WIDTH, DISPLAY_HEIGHT)

    def reset(self):
        pass

    # Animation length in frames, None -> infinite
    def length(self) -> Optional[int]:
        return 90

    def display_frame(self, left_eye, right_eye, frame_number):
        OFFSET_Y = -40
        offset_x = -20 if (frame_number // 6) % 2 == 0 else 20

        im = self.baseImage.rotate(
            0, translate=[offset_x, OFFSET_Y], fillcolor=0xFFFFFF
        )
        im1 = self.baseImage.rotate(
            0, translate=[offset_x, OFFSET_Y], fillcolor=0xFFFFFF
        )
        left_eye.image(im)
        right_eye.image(im1)

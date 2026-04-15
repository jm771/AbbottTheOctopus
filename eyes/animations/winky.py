from typing import Optional
from eyes.animations.animation import EyeAnimation
from eyes.animations.eye_image import load_and_scale_eye_image, scale_image
from eyes.display import DISPLAY_WIDTH, DISPLAY_HEIGHT
from PIL import Image


class WinkyAnimation(EyeAnimation):
    def __init__(self):
        self.normal_eye = load_and_scale_eye_image(DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.wink_eye = scale_image(
            Image.open("eyes/wink.png"), DISPLAY_WIDTH, DISPLAY_HEIGHT
        )

    def reset(self):
        pass

    def length(self) -> Optional[int]:
        return 180

    def display_frame(self, left_eye, right_eye, frame_number):
        # Start with normal eyes, then wink with the right eye.
        wink_after_frame = 60

        left_eye.image(self.normal_eye)
        if frame_number < wink_after_frame:
            right_eye.image(self.normal_eye)
        else:
            right_eye.image(self.wink_eye)

from typing import Optional
from PIL import Image
from eyes.animations.animation import EyeAnimation
from eyes.animations.eye_image import scale_image
from eyes.display import DISPLAY_WIDTH, DISPLAY_HEIGHT


CLAP_FRAMES = 30
N_CLAPS = 4
TOTAL_FRAMES = CLAP_FRAMES * N_CLAPS


class ClapAnimation(EyeAnimation):
    def __init__(self):
        self.star_eye = scale_image(
            Image.open("eyes/star.png"), DISPLAY_WIDTH, DISPLAY_HEIGHT
        )

    def reset(self):
        pass

    def length(self) -> Optional[int]:
        return TOTAL_FRAMES

    def display_frame(self, left_eye, right_eye, frame_number):
        left_eye.image(self.star_eye)
        right_eye.image(self.star_eye)

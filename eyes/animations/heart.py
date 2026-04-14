
from typing import Optional
from eyes.animations.animation import EyeAnimation
from eyes.animations.eye_image import load_and_scale_eye_image, scale_image
from adafruit_rgb_display import color565
from eyes.display import DISPLAY_WIDTH, DISPLAY_HEIGHT
from PIL import Image

WHITE = color565(0xff, 0xff, 0xff)

def centralize_image(image, offsety=10):
    center_x = DISPLAY_WIDTH // 2
    # looks better a little lower
    center_y = DISPLAY_HEIGHT // 2 + offsety

    x = center_x - image.width // 2
    y = center_y - image.height // 2
    return image.rotate(0, translate=[x, y], fillcolor=0xffffff) 

class HeartAnimation(EyeAnimation):
    def __init__(self):
        baseImage = scale_image(Image.open("eyes/heart.png"), DISPLAY_WIDTH, DISPLAY_HEIGHT)
        halfSize = centralize_image(scale_image(baseImage, baseImage.width//2, baseImage.height//2))
        thirdSize = centralize_image(scale_image(baseImage, baseImage.width//3, baseImage.height//3))
        twoThirdSize = centralize_image(scale_image(baseImage, baseImage.width * 2 // 3, baseImage.height * 2//3))
        self.images = [thirdSize, halfSize, twoThirdSize]

    def reset(self):
        pass

    # Animation length in frames, None -> infinite
    def length(self) -> Optional[int]:
        return 90

    def display_frame(self, left_eye, right_eye, frame_number):
        if (frame_number == 0):
            left_eye.fill(WHITE)
            right_eye.fill(WHITE)

        idx = (frame_number // 30) % 3
        im = self.images[idx]


        left_eye.image(im)
        right_eye.image(im)
  


from typing import Optional
from animations.animation import Animation
from animations.eye_image import load_and_scale_eye_image, scale_image
from adafruit_rgb_display import color565

WHITE = color565(0xff, 0xff, 0xff)

class HeartAnimation(Animation):
    def __init__(self, displayWidth, displayHeight):
        baseImage = load_and_scale_eye_image(displayWidth, displayHeight)
        halfSize = scale_image(baseImage, baseImage.width//2, baseImage.height//2)
        thirdSize = scale_image(baseImage, baseImage.width//3, baseImage.height//3)
        self.images = [thirdSize, halfSize, baseImage]

    def reset(self):
        pass

    # Animation length in frames, None -> infinite
    def length(self) -> Optional[int]:
        return 15

    def display_frame(self, left_eye, right_eye, frame_number):
        idx = (frame_number // 5) % 3
        im = self.images[idx]
        
        left_eye.fill(WHITE)
        right_eye.fill(WHITE)
        left_eye.image(im)
        right_eye.image(im)
  

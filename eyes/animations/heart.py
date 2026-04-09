
from typing import Optional
from animations.animation import Animation
from animations.eye_image import load_and_scale_eye_image, scale_image

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
        idx = (frame_number // 2) % 3
        im = self.images[idx]
        left_eye.fill(0xffffff)
        right_eye.fill(0xffffff)
        left_eye.image(im)
        right_eye.image(im)
  

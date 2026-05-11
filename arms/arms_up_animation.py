from typing import Optional

from arms.arm_animation import ArmAnimation
from arms.arm_controler import ArmController


class ArmsUpAnimation(ArmAnimation):
    def reset(self):
        pass

    def length(self) -> Optional[int]:
        return 180

    def display_frame(
        self, arms: list[ArmController], frame_number: int
    ):       
        START_POS = 0.5
        TOP = 0.9
        RAISE_FRAMES = 30
        WIGGLE_SIZE = 0.05
        ALTERNATE_FRAMES = 3

        # Raise hand for first 30 frames
        if frame_number <= RAISE_FRAMES:
            pos = START_POS + (TOP - START_POS) * frame_number / RAISE_FRAMES
        else:
            up_down = ((frame_number - RAISE_FRAMES) // ALTERNATE_FRAMES) % 2
            pos = (up_down * WIGGLE_SIZE) + TOP

        for arm in arms:
            arm.set_pos(pos)


from typing import Optional
from arms.arm_animation import ArmAnimation
from arms.arm_controler import ArmController

class ThumbsUpAnimation(ArmAnimation):
    def reset(self):
        pass

    def length(self) -> Optional[int]:
        return 180

    def display_frame(self, left_arm: ArmController, right_arm: ArmController, frame_number: int):
        START_POS = 0.5
        # Keep right arm neutral
        right_arm.set_pos(START_POS)

        END_POS = 1.0
        RAISE_FRAMES = 30

        # Raise left arm up, then hold at the top.
        if frame_number <= RAISE_FRAMES:
            pos = START_POS + (END_POS - START_POS) * (frame_number / RAISE_FRAMES)
        else:
            pos = END_POS

        left_arm.set_pos(pos)
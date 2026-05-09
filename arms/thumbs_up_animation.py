from typing import Optional
from arms.arm_animation import ArmAnimation
from arms.arm_controler import ArmController


class ThumbsUpAnimation(ArmAnimation):
    def reset(self):
        pass

    def length(self) -> Optional[int]:
        return 180

    def display_frame(
        self, arms: list[ArmController], frame_number: int
    ):
        left_arm = arms[0]
        right_arm = arms[-1]
        START_POS = 0.5
        # Keep right arm neutral
        right_arm.set_pos(START_POS)

        END_POS = 0.7
        RAISE_FRAMES = 60

        # Raise left arm up, then hold at the top.
        if frame_number <= RAISE_FRAMES:
            pos = START_POS + (END_POS - START_POS) * (frame_number / RAISE_FRAMES)
        else:
            pos = END_POS

        left_arm.set_pos(pos)

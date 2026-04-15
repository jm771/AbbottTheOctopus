from typing import Optional

from arms.arm_animation import ArmAnimation
from arms.arm_controler import ArmController

ACTIVE_DAB_LENGTH = 30
HOLD_DAB_LENGTH = 90
DAB_CYCLE_LENGTH = ACTIVE_DAB_LENGTH + HOLD_DAB_LENGTH
FULL_CYCLE_LENGTH = DAB_CYCLE_LENGTH


class BrainrotArmsAnimation(ArmAnimation):
    def reset(self):
        pass

    def length(self) -> Optional[int]:
        return FULL_CYCLE_LENGTH

    def display_frame(
        self, left_arm: ArmController, right_arm: ArmController, frame_number: int
    ):
        frame_number = frame_number // 2  # convert to 30 fps

        pos = [0.5, 0.5]
        t = frame_number / 30.0

        # pos 0->1 over 240 frames (4 sec @ 60hz) (starts at 0.5)
        # first 0.5 seconds: dab it (start at [0.5, 0.5], move to 0.75, 1.0)
        # 0.5, 0.5 @ 0 -> 0.75, 1.0 @ 30 = start_pos + (.25, .5)(frame / 30)
        # hold for 1.5 sec
        # t 0->1 frame 0->30
        if frame_number < ACTIVE_DAB_LENGTH:
            pos = [pos[0] + 0.25 * t, pos[1] + 0.5 * t]
        elif frame_number < ACTIVE_DAB_LENGTH + HOLD_DAB_LENGTH:
            pos = [0.75, 1.0]
        left_arm.set_pos(pos[0])
        right_arm.set_pos(pos[1])
        print(f"{frame_number}/t{t}: {pos}")

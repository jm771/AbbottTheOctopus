from typing import Optional

from arms.arm_animation import ArmAnimation
from arms.arm_controler import ArmController

FULL_CYCLE_LENGTH = 60
N_WAVES = 8
WAVE_CYCLE_LENGTH = FULL_CYCLE_LENGTH // N_WAVES
HALF_CYCLE_LENGTH = WAVE_CYCLE_LENGTH // 2


class ShockedArmsAnimation(ArmAnimation):
    def reset(self):
        pass

    def length(self) -> Optional[int]:
        return FULL_CYCLE_LENGTH

    def display_frame(self, left_arm: ArmController, right_arm: ArmController, frame_number: int):
        frame_number -= HALF_CYCLE_LENGTH // 2

        
        pos = (abs(frame_number % WAVE_CYCLE_LENGTH - HALF_CYCLE_LENGTH)) / HALF_CYCLE_LENGTH / 4
        left_arm.set_pos(pos)
        right_arm.set_pos(1-pos)

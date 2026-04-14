from typing import Optional

from arms.arm_animation import ArmAnimation
from arms.arm_controler import ArmController

FULL_CYCLE_LENGTH = 240
N_WAVES = 2
WAVE_CYCLE_LENGTH = FULL_CYCLE_LENGTH // N_WAVES
HALF_CYCLE_LENGTH = WAVE_CYCLE_LENGTH // 2


class BigWaveAnimation(ArmAnimation):
    def reset(self):
        pass

    def length(self) -> Optional[int]:
        return FULL_CYCLE_LENGTH

    def display_frame(self, left_arm: ArmController, right_arm: ArmController, frame_number: int):
        frame_number -= HALF_CYCLE_LENGTH // 2

        
        pos = (abs(frame_number % WAVE_CYCLE_LENGTH - HALF_CYCLE_LENGTH)) / HALF_CYCLE_LENGTH
        left_arm.set_pos(pos)
        right_arm.set_pos(1-pos)

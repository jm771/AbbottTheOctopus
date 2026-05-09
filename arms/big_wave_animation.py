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

    def display_frame(
        self, arms: list[ArmController], frame_number: int
    ):
        frame_number -= HALF_CYCLE_LENGTH // 2

        pos = (
            abs(frame_number % WAVE_CYCLE_LENGTH - HALF_CYCLE_LENGTH)
        ) / HALF_CYCLE_LENGTH

        for i, arm in enumerate(arms):
            arm.set_pos(pos if i % 2 == 0 else 1 - pos)

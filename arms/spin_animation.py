from typing import Optional
from math import pi, cos

from arms.arm_animation import ArmAnimation
from arms.arm_controler import ArmController

CYCLE_LENGTH = 628
N_WAVES = 2


class SpinAnimation(ArmAnimation):
    """Rotate the arms in a wave"""

    def reset(self):
        pass

    def length(self) -> Optional[int]:
        return CYCLE_LENGTH * N_WAVES

    def display_frame(
        self, arms: list[ArmController], frame_number: int
    ):
        # Current phase position, in radians
        t = (frame_number / CYCLE_LENGTH) * 2 * pi
        n = len(arms)
        for i, arm in enumerate(arms):
            # Phase offset of this arm
            theta = 2 * pi * (i / n)
            # scale [0, 1]
            pos = cos(t + theta) * 0.5 + 0.5
            arm.set_pos(pos)


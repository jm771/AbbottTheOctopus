from typing import Optional

from arms.arm_animation import ArmAnimation
from arms.arm_controler import ArmController


class IdleArmAnimation(ArmAnimation):
    def reset(self):
        pass

    def length(self) -> Optional[int]:
        return None

    # It'd probably get a bit noisy to have this moving when idle
    # TODO - I could ready the current location off the arm controlers and have it move back to neuteral more slowly
    def display_frame(
        self, arms: list[ArmController], frame_number: int
    ):
        for arm in arms:
            arm.set_pos(0.5)

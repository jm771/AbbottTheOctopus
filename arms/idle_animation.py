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
    def display_frame(self, left_arm: ArmController, right_arm: ArmController, frame_number: int):
        left_arm.set_pos(0.5)
        right_arm.set_pos(0.5)

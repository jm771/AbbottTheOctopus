from typing import Optional

from arms.arm_animation import ArmAnimation
from arms.arm_controler import ArmController

class RaiseArmsAnimation(ArmAnimation):
    def reset(self):
        pass

    def length(self) -> Optional[int]:
        return 180

    def display_frame(self, left_arm: ArmController, right_arm: ArmController, frame_number: int):
        frame_number = frame_number // 2
        START_POS = 0.5
        PUMP_BOTTOM = 0.75
        RAISE_FRAMES = 30

        # Raise hand for first 30 frames
        if frame_number <= RAISE_FRAMES:
            pos = START_POS + (PUMP_BOTTOM - START_POS) * frame_number / RAISE_FRAMES

        # then do three little pumps
        else:
            PUMP_TOP = 0.85
            # Let's so a sharp up then a slow down
            UP_FRAMES = 5
            DOWN_FRAMES = 15
            PUMP_FRAMES = UP_FRAMES + DOWN_FRAMES
            offset_frame = (frame_number - RAISE_FRAMES) % PUMP_FRAMES
            
            if offset_frame <= UP_FRAMES:
                pos = (PUMP_TOP - PUMP_BOTTOM) * (offset_frame / UP_FRAMES) + PUMP_BOTTOM
            else:
                down_frame = offset_frame - UP_FRAMES
                pos = (PUMP_BOTTOM - PUMP_TOP) * (down_frame / DOWN_FRAMES) + PUMP_TOP

        left_arm.set_pos(pos)
        right_arm.set_pos(pos)

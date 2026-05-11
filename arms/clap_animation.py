from typing import Optional
import math

from arms.arm_animation import ArmAnimation
from arms.arm_controler import ArmController

N_CLAPS = 4
CLAP_FRAMES = 60 
TOTAL_FRAMES = CLAP_FRAMES * N_CLAPS


class ClapAnimation(ArmAnimation):
    def reset(self):
        pass

    def length(self) -> Optional[int]:
        return TOTAL_FRAMES

    def display_frame(self, arms: list[ArmController], frame_number: int):
        # Both arms move together: up on the beat, back down between beats
        beat_phase = (frame_number % CLAP_FRAMES) / CLAP_FRAMES
        pos = math.sin(beat_phase * math.pi)

        arms[0].set_pos(pos)
        arms[6].set_pos(pos)

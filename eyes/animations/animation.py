from abc import ABCMeta, abstractmethod
from typing import Optional


# If you can do your animation without needing any state other than frame number - you can leave `reset` as pass
# If you want to manage more complex state (e.g. random movement) then you can store state on the class and use
# `reset` to reset it at the end of the animation.
class EyeAnimation(metaclass=ABCMeta):
    @abstractmethod
    def reset(self):
        pass

    # Animation length in frames, None -> infinite
    # Currently only the idle animation is infinite
    @abstractmethod
    def length(self) -> Optional[int]:
        pass

    # Frames are at "60hz" (a superior highly composite number) - but in practice the screen can't refresh this fast
    # allow for multiple frames advancing between calls (if you're taking the approach of frame is a pure function of
    # frame number you get this for free - if using state you need to e.g. scale your speeds)
    @abstractmethod
    # TODO - find good type hints for the adafruit driver for this
    # Abbott's left / right - i.e. stage left / right
    def display_frame(self, left_eye, right_eye, frame_number: int):
        pass

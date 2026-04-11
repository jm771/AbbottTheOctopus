from abc import ABCMeta, abstractmethod
from typing import Optional

# If you can do your animation without needing any state other than frame number - you can leave `reset` as pass
# If you want to manage more complex state (e.g. random movement) then you can store state on the class and use 
# `reset` to reset it at the end of the animation.
class Animation(metaclass=ABCMeta):
    @abstractmethod
    def reset(self):
        pass

    # Animation length in frames, None -> infinite
    # Currently only the idle animation is infinite
    @abstractmethod
    def length(self) -> Optional[int]:
        pass

    @abstractmethod
    def display_frame(self, left_eye, right_eye, frame_number):
        pass

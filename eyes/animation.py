from abc import ABCMeta, abstractmethod
from typing import Optional

class Animation(metaclass=ABCMeta):
    @abstractmethod
    def reset(self):
        pass

    # Animation length in frames, None -> infinite
    @abstractmethod
    def length(self) -> Optional[int]:
        pass

    @abstractmethod
    def display_frame(self, left_eye, right_eye, frame_number):
        pass

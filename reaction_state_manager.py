from abc import ABCMeta, abstractmethod
import enum
from typing import Optional
from eyes.animations.animation import EyeAnimation


class ReactionType(enum.Enum):
    Excited = "Excited"
    Love = "Love"

class ReactionSubManager(ABCMeta):
    @abstractmethod
    def idle(self,):
        pass

    @abstractmethod
    def get_animation_length(self, reactionType: ReactionType) -> int:
        pass

    @abstractmethod
    def start_animation(self, reactionType: ReactionType):
        pass

    @abstractmethod
    def play_animation_frame(self, frame: int):
        pass

class ArmReactionManager(ReactionSubManager):
    # We DI this because might want to test on PC with fake displays
    def __init__(self, left_display, right_display):
        self._left_display = left_display
        self._right_display = right_display

        # Could definitely have a few and pick randomly or sth
        self.idle_animation = IdleEyesAnimation()
        self.animations: dict[ReactionType, EyeAnimation] = {
            ReactionType.Excited: ExcitedAnimation(),
            ReactionType.Love: HeartAnimation()
        }
        self.active_animation: EyeAnimation = self.idle_animation

    def idle(self,):
        self.active_animation.reset()
        self.active_animation = self.idle_animation


    def get_animation_length(self, reactionType) -> int:
        len = self.animations[reactionType].length()
        assert len is not None, "Set up an infinite animation in the reactions interface"
        return len
    
    def start_animation(self, reactionType: ReactionType):
        self.active_animation.reset()
        self.active_animation = self.animations[ReactionType]


    def play_animation_frame(self, frame: int):
        self.active_animation.display_frame(self._left_display, self._right_display, frame)


def make_arm_reaction_manager():
    return ArmReactionManager(make_left_eye_display(), make_right_eye_display())

from time import sleep
import sys
import select


from eye_controllers import make_left_eye_display, make_right_eye_display
from animations.excited import ExcitedAnimation
from animations.moving_eyes import IdleEyesAnimation
from animations.heart import HeartAnimation



def play_animation(animation):
    assert animation.length() is not None, f"animation has no length - can't be played one time"
    for i in range (0, animation.length()):
        animation.display_frame(left_display, right_display, i)
        sleep(0.1)
    animation.reset()

def select_animation(character):
    if character == 'e':
        return excited_animation
    if character == 'h':
        return heart_animation

    return None

def readline_nonblocking():
    if select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.readline().rstrip()

    return None

i = 0
while True:
    animation = select_animation(readline_nonblocking())

    if animation is not None:
        idle_animation.reset()
        i = 0
        play_animation(animation)

    idle_animation.display_frame(left_display, right_display, i)
    i+=1
    sleep(0.1)


class EyesReactionManager(ReactionSubManager):
    pass

def make_eyes_reaction_manager():
    pass
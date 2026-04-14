from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
import enum
import math
from arms.arm_animation import ArmAnimation
from arms.arm_controler import make_arm_controllers
from arms.big_wave_animation import BigWaveAnimation
from arms.idle_animation import IdleArmAnimation
from arms.raise_arms_animation import RaiseArmsAnimation
from eyes.animations.animation import EyeAnimation
from eyes.eye_controllers_fb import make_left_eye_display, make_right_eye_display
from eyes.animations.excited import ExcitedAnimation
from eyes.animations.moving_eyes import IdleEyesAnimation
from eyes.animations.heart import HeartAnimation



class ReactionType:
    Excited = "Excited"
    Love = "Love"

class ReactionSubManager(metaclass=ABCMeta):
    @property
    @abstractmethod
    def name(self,):
        pass


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

class EyesReactionManager(ReactionSubManager):
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
    
    @property
    def name(self):
        return "eyes"

    def idle(self):
        self.active_animation.reset()
        self.active_animation = self.idle_animation


    def get_animation_length(self, reactionType) -> int:
        len = self.animations[reactionType].length()
        assert len is not None, "Set up an infinite animation in the reactions interface"
        return len
    
    def start_animation(self, reactionType: ReactionType):
        self.active_animation.reset()
        self.active_animation = self.animations[reactionType]


    def play_animation_frame(self, frame: int):
        # Downsample frames for now - to stop the display looking too jank
        if frame % 6 == 0:
            # loop animation if we play past the end
            looped_frame = frame if self.active_animation.length() is None else frame % self.active_animation.length()

            self.active_animation.display_frame(self._left_display, self._right_display, looped_frame)


def make_eyes_reaction_manager():
    return EyesReactionManager(make_left_eye_display(), make_right_eye_display())



class ArmsReactionManager(ReactionSubManager):
    # We DI this because might want to test on PC with fake displays
    def __init__(self, left_arm, right_arm):
        self._left_arm = left_arm
        self._right_arm = right_arm

        # Could definitely have a few and pick randomly or sth
        self.idle_animation = IdleArmAnimation()
        self.animations: dict[ReactionType, ArmAnimation] = {
            ReactionType.Excited: BigWaveAnimation(),
            ReactionType.Love: RaiseArmsAnimation()
        }
        self.active_animation: ArmAnimation = self.idle_animation

    @property
    def name(self):
        return "arms"

    def idle(self):
        self.active_animation.reset()
        self.active_animation = self.idle_animation


    def get_animation_length(self, reactionType) -> int:
        len = self.animations[reactionType].length()
        assert len is not None, "Set up an infinite animation in the reactions interface"
        return len
    
    def start_animation(self, reactionType: ReactionType):
        self.active_animation.reset()
        self.active_animation = self.animations[reactionType]


    def play_animation_frame(self, frame: int):
        # Idle if we go past the end of the animation:
        if self.active_animation.length() is None or frame < self.active_animation.length():
            self.active_animation.display_frame(self._left_arm, self._right_arm, frame)
        else:
            self.idle()

def make_arms_reaction_manager():
    return ArmsReactionManager(*make_arm_controllers())

def td_to_micros(td: timedelta):
    return td.seconds * 1_000_000 + td.microseconds

class ReactionStateManager():
    _MICROS_PER_FRAME = 1_000_000 // 60

    def __init__(self, sub_managers: list[ReactionSubManager]):
        self._sub_managers = sub_managers
        self._current_animation_length = 0
        self._queued_reactions: list[ReactionType] = []
        self._animation_start_time = datetime.now()
        self._idle()

    def _idle(self):
        self._is_idle = True
        self._last_frame = -1

        for manager in self._sub_managers:
            manager.idle()

    def _start_next_animation(self):
        new_reaction = self._queued_reactions[0]
        self._current_animation_length = max(m.get_animation_length(new_reaction) for m in self._sub_managers)
        self._animation_start_time = datetime.now()
        self._last_frame = -1

        for manager in self._sub_managers():
            manager.start_animation(new_reaction)

    def _get_current_frame(self):
        return math.floor(td_to_micros(datetime.now() - self._animation_start_time) // self._MICROS_PER_FRAME)

    def _maybe_push_animation_frame(self):
        current_frame = self._get_current_frame()
        if current_frame == self._last_frame:
            return
        if current_frame > self._last_frame + 1:
            print(f"Missed a frame rendering {current_frame}, last frame was {self._last_frame} does animation have lots of compute?")
        
        for manager in self._sub_managers:
            #start = datetime.now()
            manager.play_animation_frame(current_frame)
            #end = datetime.now()
            # print(f"manager {manager.name} took {end - start}")

        self._last_frame = current_frame
            

    def queue_reaction(self, reaction_type: ReactionType):
        if reaction_type not in self._queued_reactions:
            self._queued_reactions.append(reaction_type)

    def poll(self):
        if self._is_idle == True:
            if len(self._queued_reactions) > 0:
                self._start_next_animation()
        else:
            if self._get_current_frame() >= self._current_animation_length:
                self._queued_reactions = self._queued_reactions[1:]
                if len(self._queued_reactions == 0):
                    self._idle()
                else:
                    self._start_next_animation()

        self._maybe_push_animation_frame()


    def empty_queue(self):
        self._queued_reactions = []
        self._idle()

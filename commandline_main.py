from time import sleep
import sys
import select
from reaction_state_manager import ReactionStateManager, ReactionType, make_arms_reaction_manager, make_eyes_reaction_manager

ReactionManager = ReactionStateManager([make_eyes_reaction_manager(), make_arms_reaction_manager()])


def select_reaction(character):
    if character == 'e':
        return ReactionType.Excited
    if character == 'h':
        return ReactionType.Love
    if character == 's':
        return ReactionType.Shocked

    return None

def readline_nonblocking():
    if select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.readline().rstrip()

    return None


while True:
    reaction = select_reaction(readline_nonblocking())
    if reaction is not None:
        ReactionManager.queue_reaction(reaction)
    
    ReactionManager.poll()
    sleep(0.001)

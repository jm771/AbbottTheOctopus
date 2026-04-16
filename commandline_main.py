from time import sleep
import sys
import select
import argparse
from reaction_state_manager import (
    ReactionStateManager,
    ReactionType,
    make_arms_reaction_manager,
    make_eyes_reaction_manager,
    make_graphical_reaction_manager,
    make_octopus_reaction_manager,
)

def select_reaction(character):
    if character == "e":
        return ReactionType.Excited
    if character == "h":
        return ReactionType.Love
    if character == "s":
        return ReactionType.Shocked
    if character == "t":
        return ReactionType.ThumbsUp

    return None


def readline_nonblocking():
    if select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.readline().rstrip()

    return None


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(description='Abbott the Octopus - Commandline Control')
    parser.add_argument('--test', action='store_true',
                       help='Run in test mode with graphical window')
    args = parser.parse_args()

    # Create reaction manager based on mode
    reaction_manager = make_octopus_reaction_manager() if not args.test else make_graphical_reaction_manager()

    print(f"Running in {'TEST' if args.test else 'NORMAL'} mode")
    print("Press 'e' for Excited, 'h' for Love, 's' for Shocked, 't' for ThumbsUp")

    try:
        while True:
            reaction = select_reaction(readline_nonblocking())
            if reaction is not None:
                reaction_manager.queue_reaction(reaction)

            reaction_manager.poll()
            sleep(0.001)
    except KeyboardInterrupt:
        print("\nShutting down...")


if __name__ == "__main__":
    main()

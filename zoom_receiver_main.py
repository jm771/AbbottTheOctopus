#!/usr/bin/env python3
"""
Minimal Flask web service to receive reaction events from Zoom App backend.
"""

import threading
from time import sleep

from flask import Flask, request, jsonify
from datetime import datetime
import json
from queue import Empty, Queue

from reaction_state_manager import (
    ZOOM_EMOJI_TO_REACTION_TYPE,
    ReactionStateManager,
    make_arms_reaction_manager,
    make_eyes_reaction_manager,
)

q = Queue()
ReactionManager = ReactionStateManager(
    [make_eyes_reaction_manager(), make_arms_reaction_manager()]
)
app = Flask(__name__)


def add_reaction_to_queue(emoji_name: str):
    q.put_nowait(emoji_name)


@app.route("/reaction", methods=["POST"])
def receive_reaction():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Print timestamp and full event data
        timestamp = datetime.now().isoformat()
        print(f"\n{'='*80}")
        print(f"[{timestamp}] REACTION EVENT RECEIVED")
        print(f"{'='*80}")
        print(json.dumps(data, indent=2))
        print(f"{'='*80}\n")

        # Return success response
        add_reaction_to_queue(data["type"])

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Reaction received",
                    "timestamp": timestamp,
                }
            ),
            200,
        )


    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint.
    """
    return (
        jsonify(
            {
                "status": "healthy",
                "service": "reaction-receiver",
                "timestamp": datetime.now().isoformat(),
            }
        ),
        200,
    )


def run_flask():
    app.run(host="0.0.0.0", threaded=True, port=5000, debug=False)


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("Starting Reaction Receiver Service")
    print("=" * 80)
    print("Listening on: http://localhost:5000")
    print("Endpoint: POST http://localhost:5000/reaction")
    print("Health check: GET http://localhost:5000/health")
    print("=" * 80 + "\n")

    t = threading.Thread(target=run_flask, daemon=True)
    t.start()

    while True:
        try:
            while True:
                emoji = q.get_nowait()
                try:
                    reaction = ZOOM_EMOJI_TO_REACTION_TYPE[emoji]
                    ReactionManager.queue_reaction(reaction)
                except KeyError:
                    pass
        except Empty:
            pass

        ReactionManager.poll()
        sleep(0.001)

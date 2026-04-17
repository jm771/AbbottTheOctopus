#!/usr/bin/env python3

import argparse

from arms.arm_controler import ArmController
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json

from graphical_stubs import GraphicalStubArmController


ARM_CONTROLLERS = []

def get_arm_controllers(is_test):
    if is_test:
        return [GraphicalStubArmController(True) for i in range (0, 7)]
    else:
        import board
        import busio
        from adafruit_pca9685 import PCA9685

        i2c = board.I2C()
        pca = PCA9685(i2c)
        pca.frequency = 60
        return [
            ArmController(pca.channels[i], False) for i in range(0,8)
        ]

        return [ArmController(i, False) for i in range (0, 7)]

app = Flask(__name__)
CORS(app, origins="*")

@app.route("/arm", methods=["POST"])
def receive_reaction():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Print timestamp and full event data
        timestamp = datetime.now().isoformat()
        print(f"\n{'='*80}")
        print(json.dumps(data, indent=2))
        print(f"{'='*80}\n")

        channel = int(data["tentacle"])
        height = float(data["height"])

        ARM_CONTROLLERS[channel].set_pos(height)

        return (
            jsonify(
                {
                    "status": "success",
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

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("Starting direct control service")
    print("=" * 80)
    print("Listening on: http://localhost:5000")
    print("Endpoint: POST http://localhost:5000/reaction")
    print("Health check: GET http://localhost:5000/health")
    print("=" * 80 + "\n")

    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true',
                       help='Run in test mode with graphical window')
    args = parser.parse_args()

    # Create reaction manager based on mode
    ARM_CONTROLLERS = get_arm_controllers(args.test)

    app.run(host="0.0.0.0", port=5000, debug=True)

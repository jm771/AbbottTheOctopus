#!/usr/bin/env python3
"""
Minimal Flask web service to receive reaction events from Zoom App backend.
"""

from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/reaction', methods=['POST'])
def receive_reaction():
    """
    Receives reaction events and prints them to console.
    """
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
        return jsonify({
            'status': 'success',
            'message': 'Reaction received',
            'timestamp': timestamp
        }), 200

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    """
    return jsonify({
        'status': 'healthy',
        'service': 'reaction-receiver',
        'timestamp': datetime.now().isoformat()
    }), 200


if __name__ == '__main__':
    print("\n" + "="*80)
    print("Starting Reaction Receiver Service")
    print("="*80)
    print("Listening on: http://localhost:5000")
    print("Endpoint: POST http://localhost:5000/reaction")
    print("Health check: GET http://localhost:5000/health")
    print("="*80 + "\n")

    app.run(host='0.0.0.0', port=5000, debug=True)

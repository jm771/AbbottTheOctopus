# Reaction Receiver Service

A minimal Python Flask service that receives reaction events from the Zoom App backend.

## Setup

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running

```bash
python app.py
```

The service will start on `http://localhost:5000`

## Endpoints

- `POST /reaction` - Receives reaction events and prints them to console
- `GET /health` - Health check endpoint

## Example Output

When a reaction is received, you'll see:

```
================================================================================
[2026-03-31T21:30:45.123456] REACTION EVENT RECEIVED
================================================================================
{
  "timestamp": "2026-03-31T21:30:45.018Z",
  "eventType": "emoji_reaction",
  "participantUUID": "16A7C33B-2461-D90B-8F18-2526CD1E7651",
  "unicode": "👍",
  "meetingUUID": "abc123..."
}
================================================================================
```

## Docker (Optional)

You can also run with Docker:

```bash
docker run -p 5000:5000 -v $(pwd):/app python:3.11-slim sh -c "cd /app && pip install -r requirements.txt && python app.py"
```

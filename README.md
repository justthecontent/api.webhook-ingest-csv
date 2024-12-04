# Webhook to CSV Logger

A simple Flask-based microservice that receives webhook events and logs them to a CSV file. Built specifically for handling Slack webhooks, but can be adapted for other webhook sources.

## Features

- Receives POST requests with JSON payloads
- Logs timestamp, event type, and full payload to CSV
- Persists data using Docker volumes
- Uses Gunicorn for production-grade serving

## Setup

1. Clone the repository
2. Build and start the service:
```bash
docker compose build
docker compose up -d
```

The service will be available at `http://localhost:5001/webhook`

## Testing

The project uses pytest for testing. To run the tests:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests with coverage report
python -m pytest app/test_app.py -v --cov
```

Current test coverage is at 93% with all tests passing.

## Usage

Send webhook events using curl:

```bash
# Basic message event
curl -X POST "http://localhost:5001/webhook" \
     -H "Content-Type: application/json" \
     -H "X-Slack-Event-Type: message" \
     -d '{"type":"message","channel":"C123456","text":"Hello world"}'

# Reaction added event
curl -X POST "http://localhost:5001/webhook" \
     -H "Content-Type: application/json" \
     -H "X-Slack-Event-Type: reaction_added" \
     -d '{"type":"reaction_added","reaction":"thumbsup","item":{"channel":"C123456","ts":"1234567890.123456"}}'
```

## Viewing Logged Data

To view the contents of the CSV file:

```bash
docker compose exec webhook-service cat /data/webhook_data.csv
```

The CSV file contains three columns:
- timestamp: ISO format timestamp when the webhook was received
- event_type: Type of event from X-Slack-Event-Type header
- payload: Full JSON payload as received

## Configuration

The service uses the following default configuration:
- Internal port: 5000
- External port: 5001
- CSV file location: /data/webhook_data.csv
- Data volume: webhook-data

## Docker Components

- `Dockerfile`: Builds Python environment and installs dependencies
- `docker-compose.yml`: Defines service, port mapping, and volume
- `requirements.txt`: Python package dependencies
- `app/app.py`: Main Flask application code

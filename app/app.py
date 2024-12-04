from flask import Flask, request, jsonify
import csv
import os
from datetime import datetime
import json
import logging
from typing import Tuple, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

CSV_FILE = './data/webhook_data.csv'
CSV_HEADERS = ['timestamp', 'event_type', 'payload']

# Ensure the data directory exists
os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

# Initialize CSV file with headers if it doesn't exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADERS)

@app.route('/webhook', methods=['POST'])
def webhook() -> Tuple[Dict[str, str], int]:
    """
    Handle incoming webhook POST requests.
    
    Logs the webhook data to a CSV file with timestamp, event type, and payload.
    
    Returns:
        Tuple[Dict[str, str], int]: Response dictionary and HTTP status code
    """
    try:
        timestamp = datetime.now().isoformat()
        event_type = request.headers.get('X-Slack-Event-Type', 'unknown')
        
        if not request.is_json:
            logger.error("Received non-JSON payload")
            return {'status': 'error', 'message': 'Payload must be JSON'}, 400
        
        payload = json.dumps(request.json)
        
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, event_type, payload])
        
        logger.info(f"Webhook received - Event: {event_type}")
        return {'status': 'success'}, 200
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return {'status': 'error', 'message': 'Internal server error'}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

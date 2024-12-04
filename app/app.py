from flask import Flask, request
import csv
import os
from datetime import datetime
import json

app = Flask(__name__)

CSV_FILE = '/data/webhook_data.csv'
CSV_HEADERS = ['timestamp', 'event_type', 'payload']

# Ensure the data directory exists
os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

# Initialize CSV file with headers if it doesn't exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADERS)

@app.route('/webhook', methods=['POST'])
def webhook():
    timestamp = datetime.now().isoformat()
    event_type = request.headers.get('X-Slack-Event-Type', 'unknown')
    payload = json.dumps(request.json)
    
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, event_type, payload])
    
    return {'status': 'success'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
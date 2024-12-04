import pytest
from flask_testing import TestCase
from app import app, CSV_FILE
import os
import csv

class TestWebhook(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_directory_initialization(self):
        assert os.path.exists(os.path.dirname(CSV_FILE)), 'Directory for CSV does not exist'

    def test_csv_header_initialization(self):
        with open(CSV_FILE, 'r') as f:
            csv_reader = csv.reader(f)
            headers = next(csv_reader)
            assert headers == ['timestamp', 'event_type', 'payload'], 'CSV headers are not initialized correctly'

# more tests will be added here


    def test_valid_webhook_post(self):
        response = self.client.post('/webhook', json={'key': 'value'}, headers={'X-Slack-Event-Type': 'event_type1'})
        assert response.status_code == 200
        assert response.json['status'] == 'success', 'Webhook POST response status not successful'
        with open(CSV_FILE, 'r') as f:
            lines = f.readlines()
            assert len(lines) > 1, 'CSV file did not append data'

    def test_invalid_webhook_post(self):
        response = self.client.post('/webhook', json={'key': 'value'}, headers={})
        assert response.status_code == 200
        assert response.json['status'] == 'success', 'Webhook POST response status not successful with missing event type'
        with open(CSV_FILE, 'r') as f:
            lines = f.readlines()
            # Check if 'unknown' is used as event_type
            assert 'unknown' in lines[-1], 'Fallback event type was not used'


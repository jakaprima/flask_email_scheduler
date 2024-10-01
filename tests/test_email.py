import json
import pytest
from app.models import Email


@pytest.mark.parametrize("url, expected_status", [
    ('/', 200),
    ('/send-mail', 200)
])
def test_routes(test_client, url, expected_status):
    response = test_client.get(url)
    assert response.status_code == expected_status


def test_save_emails_success(test_client):
    # Prepare valid data
    valid_data = {
        "event_id": 1,
        "email_subject": "EMAIL_SUBJECT",
        "email_content": "EMAIL_CONTENT",
        "timestamp": "1 Oct 2024 08:44"
    }

    response = test_client.post('/api/save_emails', data=json.dumps(valid_data),
                                content_type='application/json')

    assert response.status_code == 201
    assert b'Email saved and scheduled for sending.' in response.data


def test_save_emails_invalid_timestamp(test_client):
    # Prepare invalid data
    invalid_data = {
        "event_id": 1,
        "email_subject": "EMAIL_SUBJECT",
        "email_content": "EMAIL_CONTENT",
        "timestamp": "invalid-timestamp"  # Invalid timestamp
    }

    response = test_client.post('/api/save_emails', data=json.dumps(invalid_data),
                                content_type='application/json')
    response_json = response.json

    assert response.status_code == 420
    assert response_json['message_action'] == 'INVALID_REQUEST_PARAMETER'


def test_save_emails_missing_fields(test_client):
    # Prepare data missing required fields
    missing_fields_data = {
        "email_subject": "EMAIL_SUBJECT",
    }

    response = test_client.post('/api/save_emails', data=json.dumps(missing_fields_data),
                                content_type='application/json')
    response_json = response.json
    print("RES", response_json)
    assert response.status_code == 420
    assert response_json['message_action'] == 'INVALID_REQUEST_PARAMETER'
    missing_list = ['event_id', 'email_content', 'timestamp']
    for data in response_json['message_data']:
        assert data['description'] == 'Missing data for required field.'
        assert data['key'] in missing_list

# test_myapp.py

import pytest
from app import app

@pytest.fixture
def client():
    """Create and configure a new app instance for each test."""
    app.config['TESTING'] = True  # Enable testing mode for error catching
    with app.test_client() as client:
        yield client  # This client will be used for making requests to your app

def test_process_data_endpoint(client):
    """Test the /process_data endpoint to ensure it processes data correctly."""
    # Mock data for testing
    data = {'file_path': 'test_dataset.xlsx'}
    
    # Send a POST request to the endpoint
    response = client.post('/process_data', json=data)
    
    # Check if the response status code is 200
    assert response.status_code == 200
    
    # Check if the response contains insights
    assert 'insights' in response.json

    # Add more assertions as needed to verify the response content

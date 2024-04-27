# test_myapp.py

import pytest
from myapp import app

@pytest.fixture
def client():
    """Create and configure a new app instance for each test."""
    app.config['TESTING'] = True  # Enable testing mode for error catching
    with app.test_client() as client:
        yield client  # This client will be used for making requests to your app

def test_index_route(client):
    """Test the root URL route to ensure it returns a 200 status and the expected content."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data  # Ensure response contains 'Welcome'

# Add more test functions to cover other routes and functionalities

def test_process_data_endpoint(client):
    """Test the /process_data endpoint with a sample file to ensure it processes data correctly."""
    # You can mock the file upload using Werkzeug's FileStorage
    with open('test_data.csv', 'rb') as file:
        data = {'file': (file, 'test_data.csv')}
        response = client.post('/process_data', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 200
    # Add assertions to verify the response content

# Add more test functions to cover other aspects of your application's functionality

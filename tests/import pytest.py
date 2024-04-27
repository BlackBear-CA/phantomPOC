import pytest
from myapp import app  # Replace 'myapp' with the actual module name of your Flask app

@pytest.fixture
def client():
    """Create and configure a new app instance for each test."""
    app.config['TESTING'] = True  # Enable testing mode for error catching
    with app.test_client() as client:
        yield client  # This client will be used for making requests to your app

def test_home_page(client):
    """Test the home page route to ensure it returns a 200 status and the expected content."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data  # Ensure response contains 'Welcome'


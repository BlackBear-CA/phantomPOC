import pytest
from myapp import app # Replace 'myapp' with the name of your Flask app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test the home page route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data  # Adjust based on your expected response

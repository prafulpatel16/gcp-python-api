"""Unit tests for FastAPI app"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    """Test the /helloworld endpoint"""
    response = client.get("/helloworld")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_health_check():
    """Test the /healthz endpoint"""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


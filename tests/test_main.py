"""Unit tests for FastAPI app"""

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_read_root():
    """Test for GET /"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "Hello, World! Status: OK"

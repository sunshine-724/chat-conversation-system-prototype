from fastapi.testclient import TestClient
import sys
import os

# Add backend to sys.path
sys.path.append('/home/sunshine724/development-linux/researach/chat-conversation-system-prototype/backend')

from main import app

client = TestClient(app)

def test_get_models():
    response = client.get("/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert isinstance(data["models"], list)
    assert len(data["models"]) > 0
    print("Models endpoint verification successful!")
    print("Available models:", data["models"])

if __name__ == "__main__":
    test_get_models()

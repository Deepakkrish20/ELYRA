import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_analyze_spam_ham():
    # Test safe message
    response = client.post("/api/spam/analyze", json={"text": "Hello, how are you today?"})
    assert response.status_code == 200
    data = response.json()
    assert data["is_spam"] is False
    assert "safe" in data["message"]

    # Test spam message
    response = client.post("/api/spam/analyze", json={"text": "Claim your FREE prize money now!"})
    assert response.status_code == 200
    data = response.json()
    assert data["is_spam"] is True
    assert "spam" in data["message"]

def test_analyze_poem():
    response = client.post("/api/poem/analyze", json={"text": "Two roads diverged..."})
    assert response.status_code == 200
    data = response.json()
    assert "emotions" in data
    assert "morals" in data
    assert "poetic_devices" in data
    assert data["emotions"]["Nostalgia"] == 0.84

def test_analyze_movie():
    response = client.post("/api/movie/analyze", json={"synopsis": "A space adventure..."})
    assert response.status_code == 200
    data = response.json()
    assert "genres" in data
    assert "advisories" in data
    assert len(data["genres"]) == 3
    assert data["genres"][0]["name"] == "Sci-Fi"

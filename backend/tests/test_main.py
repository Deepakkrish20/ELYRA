import os
import json
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_keyword_store():
    # Reset store to clean state before every single test!
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app", "data"))
    store_file = os.path.join(data_dir, "keyword_store.json")
    initial_data = {
        "total_spam_messages": 0,
        "total_ham_messages": 0,
        "keyword_counts": {}
    }
    os.makedirs(data_dir, exist_ok=True)
    with open(store_file, "w") as f:
        json.dump(initial_data, f, indent=2)
    yield


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

    # Test ham message that was incorrectly flagged due to imbalanced training counts
    response = client.post("/api/spam/analyze", json={"text": "Lol your always so convincing."})
    assert response.status_code == 200
    data = response.json()
    assert data["is_spam"] is False
    assert "safe" in data["message"]

def test_analyze_poem():
    response = client.post("/api/poem/analyze", json={"text": "Two roads diverged..."})
    assert response.status_code == 200
    data = response.json()
    assert "emotions" in data
    assert "morals" in data
    assert "poetic_devices" in data
    assert data["emotions"]["Nostalgia"] == 0.84

def test_analyze_movie():
    # Test known movie in the database
    payload = {
        "title": "Inception",
        "year": "2010"
    }
    response = client.post("/api/movie/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Inception"
    assert data["year"] == "2010"
    assert data["genres"][0]["name"] == "Sci-Fi"
    assert data["watchability_status"] == "Highly Recommended"
    assert "subconscious" in data["summary"]

    # Test custom/dynamic movie
    payload = {
        "title": "Space Battle of Mars",
        "year": "2026"
    }
    response = client.post("/api/movie/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Space Battle Of Mars"
    assert data["year"] == "2026"
    assert any(g["name"] == "Sci-Fi" for g in data["genres"])

def test_spam_feedback_correction():
    text = "Hey friend, are we still meeting for lunch tomorrow?"
    
    response = client.post("/api/spam/analyze", json={"text": text})
    assert response.status_code == 200
    initial_data = response.json()
    assert initial_data["is_spam"] is False
    
    feedback_response = client.post(
        "/api/spam/feedback", 
        json={
            "text": text,
            "was_spam": initial_data["is_spam"],
            "is_spam": not initial_data["is_spam"]
        }
    )
    assert feedback_response.status_code == 200
    feedback_data = feedback_response.json()
    assert feedback_data["is_spam"] is True
    
    response_after = client.post("/api/spam/analyze", json={"text": text})
    assert response_after.status_code == 200
    data_after = response_after.json()
    assert data_after["is_spam"] is True

def test_spam_automatic_barbie_classification():
    text = "Did you hear about the new Divorce Barbie? It comes with Ken's stuff."
    response = client.post("/api/spam/analyze", json={"text": text})
    assert response.status_code == 200
    data = response.json()
    assert data["is_spam"] is True
    assert "spam" in data["message"].lower()

def test_user_input_logging():
    text = "Unique test message to verify logging."
    response = client.post("/api/spam/analyze", json={"text": text})
    assert response.status_code == 200
    
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app", "data"))
    log_file = os.path.join(data_dir, "user_inputs_history.json")
    
    assert os.path.exists(log_file)
    with open(log_file, "r") as f:
        history = json.load(f)
        
    assert any(entry["text"] == text for entry in history)

def test_analyze_movie_theri():
    payload = {
        "title": "Theri",
        "year": "2016"
    }
    response = client.post("/api/movie/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Theri"
    assert data["year"] == "2016"
    assert any(g["name"] == "Action" for g in data["genres"])
    assert any(g["name"] == "Thriller" for g in data["genres"])
    assert "157 mins" in data["runtime_estimate"] or "158 mins" in data["runtime_estimate"]







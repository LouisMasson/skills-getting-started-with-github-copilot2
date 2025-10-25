import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200
    assert b"Mergington High School" in response.content


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "participants" in data["Chess Club"]


def test_signup_success():
    # Use a test email not in the list
    response = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]


def test_signup_already_signed_up():
    # First sign up
    client.post("/activities/Chess Club/signup?email=duplicate@mergington.edu")
    # Try again
    response = client.post("/activities/Chess Club/signup?email=duplicate@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent Activity/signup?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_success():
    # First sign up
    client.post("/activities/Programming Class/signup?email=unregistertest@mergington.edu")
    # Then unregister
    response = client.delete("/activities/Programming Class/signup?email=unregistertest@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "unregistertest@mergington.edu" in data["message"]


def test_unregister_not_signed_up():
    response = client.delete("/activities/Chess Club/signup?email=notsignedup@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]


def test_unregister_activity_not_found():
    response = client.delete("/activities/Nonexistent Activity/signup?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]
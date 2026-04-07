import pytest
from fastapi.testclient import TestClient
from src.app import app

def test_signup_success(client, reset_activities):
    """Test successful signup for an activity"""
    # Arrange
    new_email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": new_email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    assert new_email in data["message"]

def test_signup_adds_participant(client, reset_activities):
    """Test that signup actually adds the participant"""
    # Arrange
    new_email = "testuser@mergington.edu"

    # Act
    response = client.post(
        "/activities/Programming%20Class/signup",
        params={"email": new_email}
    )

    # Assert
    assert response.status_code == 200

    # Verify participant was added
    get_response = client.get("/activities")
    activities = get_response.json()
    assert new_email in activities["Programming Class"]["participants"]

def test_signup_duplicate_student(client, reset_activities):
    """Test that duplicate signup is rejected"""
    # Arrange - michael@mergington.edu is already signed up for Chess Club

    # Act
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "michael@mergington.edu"}  # Already signed up
    )

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_nonexistent_activity(client, reset_activities):
    """Test signup fails for non-existent activity"""
    # Arrange
    email = "test@mergington.edu"

    # Act
    response = client.post(
        "/activities/Fake%20Club/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_signup_multiple_students(client, reset_activities):
    """Test multiple signup requests work independently"""
    # Arrange
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"

    # Act
    response1 = client.post(
        "/activities/Gym%20Class/signup",
        params={"email": email1}
    )
    response2 = client.post(
        "/activities/Gym%20Class/signup",
        params={"email": email2}
    )

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200

    # Verify both were added
    get_response = client.get("/activities")
    activities = get_response.json()
    assert email1 in activities["Gym Class"]["participants"]
    assert email2 in activities["Gym Class"]["participants"]
import pytest
from fastapi.testclient import TestClient
from src.app import app

def test_remove_participant_success(client, reset_activities):
    """Test successful removal of a participant"""
    # Arrange
    email_to_remove = "michael@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Chess%20Club/participants/michael%40mergington.edu"
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Removed" in data["message"]
    assert email_to_remove in data["message"]

def test_remove_participant_removes_from_list(client, reset_activities):
    """Test that remove actually removes the participant from the list"""
    # Arrange
    email_to_remove = "emma@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Programming%20Class/participants/emma%40mergington.edu"
    )

    # Assert
    assert response.status_code == 200

    # Verify participant was removed
    get_response = client.get("/activities")
    activities = get_response.json()
    assert email_to_remove not in activities["Programming Class"]["participants"]

def test_remove_participant_not_found(client, reset_activities):
    """Test removing a participant that doesn't exist"""
    # Arrange
    nonexistent_email = "nonexistent@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Chess%20Club/participants/nonexistent%40mergington.edu"
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Participant not found" in data["detail"]

def test_remove_participant_activity_not_found(client, reset_activities):
    """Test removing participant from non-existent activity"""
    # Arrange
    email = "test@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Fake%20Club/participants/test%40mergington.edu"
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_remove_participant_multiple_removals(client, reset_activities):
    """Test removing multiple participants from the same activity"""
    # Arrange
    email1 = "john@mergington.edu"
    email2 = "olivia@mergington.edu"

    # Act
    response1 = client.delete(
        "/activities/Gym%20Class/participants/john%40mergington.edu"
    )
    response2 = client.delete(
        "/activities/Gym%20Class/participants/olivia%40mergington.edu"
    )

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200

    # Verify both were removed
    get_response = client.get("/activities")
    activities = get_response.json()
    assert email1 not in activities["Gym Class"]["participants"]
    assert email2 not in activities["Gym Class"]["participants"]
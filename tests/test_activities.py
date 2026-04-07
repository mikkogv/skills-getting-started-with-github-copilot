import pytest
from fastapi.testclient import TestClient
from src.app import app

def test_get_all_activities(client, reset_activities):
    """Test GET /activities returns all activities"""
    # Arrange - fixtures handle setup

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert len(data) == 9

def test_get_activities_structure(client, reset_activities):
    """Test GET /activities returns proper data structure"""
    # Arrange - fixtures handle setup

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    # Verify each activity has required fields
    for activity_name, details in activities.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)

def test_activity_participants_count(client, reset_activities):
    """Test specific activity participants are returned"""
    # Arrange - fixtures handle setup

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    chess_club = activities["Chess Club"]
    assert len(chess_club["participants"]) == 2
    assert "michael@mergington.edu" in chess_club["participants"]

def test_activity_max_participants(client, reset_activities):
    """Test activities have correct max participant limits"""
    # Arrange - fixtures handle setup

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    assert activities["Chess Club"]["max_participants"] == 12
    assert activities["Gym Class"]["max_participants"] == 30
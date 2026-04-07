import pytest
from fastapi.testclient import TestClient
from src.app import app

def test_get_root_redirects(client):
    """Test GET / redirects to static files"""
    # Arrange - fixtures handle setup

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"

def test_get_root_redirects_with_follow(client):
    """Test GET / redirects and follows to static files"""
    # Arrange - fixtures handle setup

    # Act
    response = client.get("/", follow_redirects=True)

    # Assert
    assert response.status_code == 200
    # Note: In a real test environment, this would serve the HTML file
    # For now, we just verify the redirect works
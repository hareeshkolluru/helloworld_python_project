"""Tests for API routes"""

from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient) -> None:
    """Test the root endpoint returns expected response."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data


def test_health_check(client: TestClient) -> None:
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data


def test_hello_without_name(client: TestClient) -> None:
    """Test the hello endpoint without name parameter."""
    response = client.get("/api/v1/hello")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Hello!" in data["message"]
    assert data["name"] is None


def test_hello_with_name(client: TestClient) -> None:
    """Test the hello endpoint with name parameter."""
    response = client.get("/api/v1/hello?name=John")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "John" in data["message"]
    assert data["name"] == "John"

import pytest
from fastapi import status

def test_connect_endpoint(client, mock_mcp, test_connection_params):
    """Test the MCP connect endpoint."""
    response = client.post("/mcp/connect", json=test_connection_params)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "connected"}

def test_connect_endpoint_invalid_params(client):
    """Test the MCP connect endpoint with invalid parameters."""
    response = client.post("/mcp/connect", json={"invalid": "params"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_send_message_endpoint(client, mock_mcp, test_message):
    """Test the MCP send message endpoint."""
    response = client.post("/mcp/send", json=test_message)
    assert response.status_code == status.HTTP_200_OK
    assert "status" in response.json()
    assert "response" in response.json()

def test_send_message_endpoint_invalid_message(client):
    """Test the MCP send message endpoint with invalid message."""
    response = client.post("/mcp/send", json={"invalid": "message"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_status_endpoint(client):
    """Test the MCP status endpoint."""
    response = client.get("/mcp/status")
    assert response.status_code == status.HTTP_200_OK
    assert "status" in response.json()
    assert "connections" in response.json()

def test_disconnect_endpoint(client):
    """Test the MCP disconnect endpoint."""
    response = client.post("/mcp/disconnect")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "disconnected"} 
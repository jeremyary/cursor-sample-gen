import pytest
from fastapi.testclient import TestClient
from app import app
from fastmcp import FastMCP

@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)

@pytest.fixture
def mock_mcp(mocker):
    """Create a mock FastMCP instance."""
    mock = mocker.Mock(spec=FastMCP)
    return mock

@pytest.fixture
def test_connection_params():
    """Sample connection parameters for testing."""
    return {
        "host": "test-mcp-server",
        "port": 1234,
        "username": "test-user",
        "password": "test-pass"
    }

@pytest.fixture
def test_message():
    """Sample message for testing."""
    return {
        "type": "test-message",
        "content": "Hello, MCP!",
        "metadata": {"test": True}
    } 
import pytest
from fastapi.testclient import TestClient
from task_flow_api.main import app


@pytest.fixture
def api_client():
    with TestClient(app) as test_client:
        yield test_client

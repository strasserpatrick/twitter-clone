from unittest.mock import MagicMock

import pytest
from starlette.testclient import TestClient

from owntwitter.api.endpoints import get_db_service
from owntwitter.app import app
from owntwitter.models.settings import Settings
from owntwitter.services.db import DatabaseConnector

settings = Settings()
url = f"http://localhost:{settings.uvicorn_port}/api"


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db_service_dependency_override():
    mock = MagicMock(spec=DatabaseConnector)

    app.dependency_overrides[get_db_service] = lambda: mock
    return mock

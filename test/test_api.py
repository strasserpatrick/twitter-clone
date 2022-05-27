from unittest.mock import MagicMock

import pytest
import requests

from owntwitter.api.endpoints import get_db_service
from owntwitter.app import app
from owntwitter.models.factories import PostFactory
from owntwitter.models.settings import Settings
from owntwitter.services.db import DatabaseConnector

settings = Settings()
url = f"http://localhost:{settings.uvicorn_port}"


@pytest.fixture
def db_service_dependency_override():
    mock = MagicMock(spec=DatabaseConnector)

    # mock adjustment here
    mock.read_recent_posts.return_value = PostFactory.batch(20)

    app.dependency_overrides[get_db_service] = lambda: mock
    return mock


def test_feed_endpoint(db_service_dependency_override):
    r = requests.get(url + "/api/feed")
    assert r.status_code == 200
    # problem: return with _id and not post_id



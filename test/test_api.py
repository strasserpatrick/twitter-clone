from unittest.mock import MagicMock

import pytest
import requests

from owntwitter.api.endpoints import get_db_service
from owntwitter.app import app
from owntwitter.models.factories import PostFactory
from owntwitter.models.models import Post
from owntwitter.models.settings import Settings
from owntwitter.services.db import DatabaseConnector

settings = Settings()
url = f"http://localhost:{settings.uvicorn_port}/api"


@pytest.fixture
def db_service_dependency_override():
    mock = MagicMock(spec=DatabaseConnector)

    # mock adjustment here
    mock.read_recent_posts.return_value = PostFactory.batch(20)

    app.dependency_overrides[get_db_service] = lambda: mock
    return mock


def test_feed_endpoint(db_service_dependency_override):
    r = requests.get(url + "/feed")

    post_list = [Post(**post_dict) for post_dict in r.json()]

    assert r.status_code == 200
    assert len(post_list) == 20


def test_get_post_not_in_db(db_service_dependency_override):
    post = PostFactory.build()
    db_service_dependency_override.read_post.return_value = post
    # dependency injection not working

    r = requests.get(url + f"/posts/{post.post_id}")

    assert r.status_code == 500



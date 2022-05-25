import pytest

from owntwitter.models.exceptions import UserNotFoundException
from owntwitter.models.factories import PostFactory, UserFactory
from owntwitter.services.db import DatabaseConnector


@pytest.fixture
def get_db():
    return DatabaseConnector()


def test_create_new_post(get_db):
    user = UserFactory.build()
    get_db.create_new_user(user)
    post = PostFactory.build()
    post.username = user.username

    res = get_db.create_new_post(post)

    assert res.acknowledged == True
    assert res.inserted_id == post.post_id


def test_create_new_post_user_not_found(get_db):
    post = PostFactory.build()
    with pytest.raises(UserNotFoundException):
        get_db.create_new_post(post)


def test_read_posts_of_user(get_db):
    user = UserFactory.build()
    get_db.create_new_user(user)
    posts = PostFactory.batch(20)

    for p in posts:
        p.username = user.username
        get_db.create_new_post(p)

    post_list = get_db.read_posts_of_user(user.username)
    assert post_list == posts



import pytest as pytest
from pymongo.errors import DuplicateKeyError

from owntwitter.models.exceptions import UserNotFoundException
from owntwitter.models.factories import CommentFactory, PostFactory, UserFactory
from owntwitter.services.db import DatabaseConnector


@pytest.fixture
def get_db():
    return DatabaseConnector()


def test_create_new_user(get_db):
    user = UserFactory.build()
    res = get_db.create_new_user(user)

    assert res.acknowledged
    assert res.inserted_id == user.username


def test_create_duplicate(get_db):
    user = UserFactory.build()
    res = get_db.create_new_user(user)

    assert res.acknowledged
    assert res.inserted_id == user.username

    # Insert duplicate
    with pytest.raises(DuplicateKeyError):
        get_db.create_new_user(user)


def test_read_user(get_db):
    users = UserFactory.batch(10)  # fill database
    [get_db.create_new_user(u) for u in users]

    for u in users:
        response_user = get_db.read_user(u.username)
        assert response_user == u


def test_read_user_not_fount(get_db):
    user = UserFactory.build()
    with pytest.raises(UserNotFoundException):
        get_db.read_user(user.username)


def test_update_user(get_db):
    old_user = UserFactory.build()
    get_db.create_new_user(old_user)

    new_user = UserFactory.build()
    new_user.username = old_user.username

    with pytest.raises(UserNotFoundException):
        get_db.update_user(new_user)



def test_update_user_not_found(get_db):
    user = UserFactory.build()
    new_user = UserFactory.build()
    new_user.username = user.username

    response = get_db.update_user(new_user)

    assert response.acknowledged
    assert response.raw_result["updatedExisting"] is False

    with pytest.raises(UserNotFoundException):
        get_db.read_user(new_user.username)


def test_delete_user(get_db):
    user = UserFactory.build()
    get_db.create_new_user(user)

    response = get_db.delete_user(user.username)
    assert response.acknowledged
    assert response.deleted_count == 1


def test_delete_user_not_found(get_db):
    user = UserFactory.build()
    with pytest.raises(UserNotFoundException):
        get_db.delete_user(user.username)


def test_delete_user_trigger(get_db):
    user = UserFactory.build()
    get_db.create_new_user(user)

    posts = PostFactory.batch(10)

    for p in posts:
        p.username = user.username
        get_db.create_new_post(p)

    comments = CommentFactory.batch(20)
    for c in comments:
        c.username = user.username
        c.post_id = posts[0].post_id
        get_db.create_new_comment(c)

    response = get_db.delete_user(user.username)
    assert response.acknowledged
    assert response.deleted_count == 1

    with pytest.raises(UserNotFoundException):
        get_db.read_user(user.username)

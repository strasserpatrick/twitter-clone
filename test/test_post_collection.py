import datetime

import pytest

from owntwitter.models.exceptions import PostNotFoundException, UserNotFoundException
from owntwitter.models.factories import CommentFactory, PostFactory, UserFactory
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

    assert res.acknowledged
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


def test_read_posts_user_not_found(get_db):
    user = UserFactory.build()
    with pytest.raises(UserNotFoundException):
        get_db.read_posts_of_user(user.username)


def test_read_posts_no_posts(get_db):
    user = UserFactory.build()
    get_db.create_new_user(user)
    post_list = get_db.read_posts_of_user(user.username)
    assert post_list == []


def test_read_post(get_db):
    user = UserFactory.build()
    post = PostFactory.build()
    post.username = user.username
    get_db.create_new_user(user)
    get_db.create_new_post(post)

    response_post = get_db.read_post(post.post_id)
    assert response_post == post


def test_read_post_not_found(get_db):
    post = PostFactory.build()
    with pytest.raises(PostNotFoundException):
        get_db.read_post(post.post_id)


def test_read_recent_posts(get_db):
    user = UserFactory.build()
    get_db.create_new_user(user)
    posts = PostFactory.batch(100)
    for p in posts:
        p.timestamp = datetime.datetime.now()
        p.username = user.username
        get_db.create_new_post(p)

    recent_posts = get_db.read_recent_posts(100)
    for p in posts:
        assert p in recent_posts


def test_update_post(get_db):
    user = UserFactory.build()
    get_db.create_new_user(user)

    old_post = PostFactory.build()
    old_post.username = user.username
    get_db.create_new_post(old_post)

    new_post = PostFactory.build()
    new_post.post_id = old_post.post_id

    response = get_db.update_post(new_post)
    assert response.acknowledged
    assert response.raw_result["updatedExisting"]
    assert get_db.read_post(old_post.post_id) == new_post


def test_update_post_not_found(get_db):
    post = PostFactory.build()
    new_post = PostFactory.build()
    new_post.post_id = post.post_id

    response = get_db.update_post(new_post)

    assert response.acknowledged
    assert not response.raw_result["updatedExisting"]

    with pytest.raises(PostNotFoundException):
        get_db.read_post(post.post_id)


def test_delete_post(get_db):
    user = UserFactory.build()
    get_db.create_new_user(user)

    post = PostFactory.build()
    post.username = user.username
    get_db.create_new_post(post)

    response = get_db.delete_post(post.post_id)
    assert response.acknowledged
    assert response.deleted_count == 1


def test_delete_post_not_found(get_db):
    post = PostFactory.build()
    response = get_db.delete_post(post.post_id)

    assert response.acknowledged
    assert response.deleted_count == 0


def test_delete_post_trigger(get_db):
    user = UserFactory.build()
    get_db.create_new_user(user)

    post = PostFactory.build()
    post.username = user.username
    get_db.create_new_post(post)

    comments = CommentFactory.batch(20)
    for c in comments:
        c.username = user.username
        c.post_id = post.post_id
        get_db.create_new_comment(c)

    response = get_db.delete_post(post.post_id)
    assert response.acknowledged
    assert response.deleted_count == 1

    assert len(get_db.read_comments_of_post(post.post_id)) == 0

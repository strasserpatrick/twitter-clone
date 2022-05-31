from typing import List

import pytest
from pymongo.errors import DuplicateKeyError

from owntwitter.models.exceptions import (
    CommentNotFoundException,
    PostNotFoundException,
    UserNotFoundException,
)
from owntwitter.models.factories import CommentFactory, PostFactory, UserFactory
from owntwitter.models.models import Comment
from owntwitter.services.db import DatabaseConnector


@pytest.fixture
def get_db():
    return DatabaseConnector()


def test_create_comment(get_db):
    user = UserFactory.build()
    get_db.create_new_user(user)

    post = PostFactory.build()
    post.username = user.username
    get_db.create_new_post(post)

    comment = CommentFactory.build()
    comment.username = user.username
    comment.post_id = post.post_id

    res = get_db.create_new_comment(comment)

    assert res.acknowledged
    assert res.inserted_id == comment.comment_id

def test_create_comment_duplicate(get_db):
    user = UserFactory.build()
    get_db.create_new_user(user)

    post = PostFactory.build()
    post.username = user.username
    get_db.create_new_post(post)

    comment = CommentFactory.build()
    comment.username = user.username
    comment.post_id = post.post_id

    res = get_db.create_new_comment(comment)

    assert res.acknowledged
    assert res.inserted_id == comment.comment_id

    with pytest.raises(DuplicateKeyError):
        get_db.create_new_comment(comment)


def test_create_comment_no_user_and_post(get_db):
    comment = CommentFactory.build()
    with pytest.raises(UserNotFoundException):
        get_db.create_new_comment(comment)


def test_read_comment(get_db):
    user = UserFactory.build()
    post = PostFactory.build()
    post.username = user.username
    comment = CommentFactory.build()
    comment.username = user.username
    comment.post_id = post.post_id

    get_db.create_new_user(user)
    get_db.create_new_post(post)
    get_db.create_new_comment(comment)

    res = get_db.read_comment(comment.comment_id)

    assert res == comment


def test_read_comment_not_found(get_db):
    comment = CommentFactory.build()

    with pytest.raises(CommentNotFoundException):
        get_db.read_comment(comment.comment_id)


def test_read_comments_of_post(get_db):
    user = UserFactory.build()
    get_db.create_new_user(user)

    post = PostFactory.build()
    post.username = user.username
    get_db.create_new_post(post)

    comments = CommentFactory.batch(10)
    for c in comments:
        c.username = user.username
        c.post_id = post.post_id
        get_db.create_new_comment(c)

    response_list = get_db.read_comments_of_post(post.post_id)
    assert comments == response_list


def test_read_comments_of_post_not_found(get_db):
    post = PostFactory.build()

    with pytest.raises(PostNotFoundException):
        get_db.read_comments_of_post(post.post_id)


def test_read_comments_of_user(get_db):
    user = UserFactory.build()
    get_db.create_new_user(user)

    post = PostFactory.build()
    post.username = user.username
    get_db.create_new_post(post)

    comments = CommentFactory.batch(10)
    for c in comments:
        c.username = user.username
        c.post_id = post.post_id
        get_db.create_new_comment(c)

    response_list = get_db.read_comments_of_post(post.post_id)
    assert comments == response_list


def test_read_comments_of_user_not_found(get_db):
    user = UserFactory.build()

    res = get_db.read_comments_of_user(user.username)
    assert not res


def test_update_comment(get_db):
    user = UserFactory.build()
    get_db.create_new_user(user)

    post = PostFactory.build()
    post.username = user.username
    get_db.create_new_post(post)

    old_comment = CommentFactory.build()
    old_comment.username = user.username
    old_comment.post_id = post.post_id
    get_db.create_new_comment(old_comment)

    new_comment = CommentFactory.build()
    new_comment.comment_id = old_comment.comment_id
    new_comment.post_id = old_comment.post_id
    new_comment.username = old_comment.username

    response = get_db.update_comment(new_comment)
    assert response.acknowledged
    assert response.raw_result["updatedExisting"]
    assert get_db.read_comment(old_comment.comment_id) == new_comment


def test_update_comment_not_found(get_db):
    comment = CommentFactory.build()
    new_comment = CommentFactory.build()
    new_comment.comment_id = comment.comment_id

    response = get_db.update_comment(new_comment)

    assert response.acknowledged
    assert not response.raw_result["updatedExisting"]

    with pytest.raises(CommentNotFoundException):
        get_db.read_comment(comment.comment_id)


def test_delete_comment(get_db):
    user = UserFactory.build()
    get_db.create_new_user(user)

    post = PostFactory.build()
    post.username = user.username
    get_db.create_new_post(post)

    comment = CommentFactory.build()
    comment.username = user.username
    comment.post_id = post.post_id
    get_db.create_new_comment(comment)

    response = get_db.delete_comment(comment.comment_id)

    assert response.acknowledged
    assert response.deleted_count == 1

    with pytest.raises(CommentNotFoundException):
        get_db.read_comment(comment.comment_id)


def test_delete_comment_not_in_db(get_db):
    user = UserFactory.build()
    get_db.create_new_user(user)

    post = PostFactory.build()
    post.username = user.username
    get_db.create_new_post(post)

    comment = CommentFactory.build()
    comment.username = user.username
    comment.post_id = post.post_id
    get_db.create_new_comment(comment)

    response = get_db.delete_comment(comment.comment_id)

    assert response.acknowledged
    assert response.deleted_count == 1

    with pytest.raises(CommentNotFoundException):
        get_db.read_comment(comment.comment_id)

    with pytest.raises(CommentNotFoundException):
        get_db.delete_comment(comment.comment_id)

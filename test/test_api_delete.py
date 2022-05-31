from conftest import url

from owntwitter.models.exceptions import (
    CommentNotFoundException,
    PostNotFoundException,
    UserNotFoundException,
)
from owntwitter.models.factories import CommentFactory, PostFactory, UserFactory


def test_delete_user(client, db_service_dependency_override):
    user = UserFactory.build()

    r = client.post(url + f"/delete/user/{user.username}")
    assert r.status_code == 203


def test_delete_user_not_found(client, db_service_dependency_override):
    user = UserFactory.build()

    db_service_dependency_override.delete_user.side_effect = UserNotFoundException

    r = client.post(url + f"/delete/user/{user.username}")
    assert r.status_code == 404


def test_delete_post(client, db_service_dependency_override):
    post = PostFactory.build()

    r = client.post(url + f"/delete/post/{post.post_id}")
    assert r.status_code == 203


def test_delete_post_not_found(client, db_service_dependency_override):
    post = PostFactory.build()

    db_service_dependency_override.delete_post.side_effect = PostNotFoundException

    r = client.post(url + f"/delete/post/{post.post_id}")
    assert r.status_code == 404


def test_delete_post_user_not_found(client, db_service_dependency_override):
    post = PostFactory.build()

    db_service_dependency_override.delete_post.side_effect = UserNotFoundException

    r = client.post(url + f"/delete/post/{post.post_id}")
    assert r.status_code == 404


def test_delete_comment(client, db_service_dependency_override):
    comment = CommentFactory.build()

    r = client.post(url + f"/delete/comment/{comment.comment_id}")
    assert r.status_code == 203


def test_delete_comment_not_found(client, db_service_dependency_override):
    comment = CommentFactory.build()

    db_service_dependency_override.delete_comment.side_effect = CommentNotFoundException

    r = client.post(url + f"/delete/comment/{comment.comment_id}")
    assert r.status_code == 404


def test_delete_comment_user_not_found(client, db_service_dependency_override):
    comment = CommentFactory.build()

    db_service_dependency_override.delete_comment.side_effect = UserNotFoundException

    r = client.post(url + f"/delete/comment/{comment.comment_id}")
    assert r.status_code == 404


def test_delete_comment_post_not_found(client, db_service_dependency_override):
    comment = CommentFactory.build()

    db_service_dependency_override.delete_comment.side_effect = PostNotFoundException

    r = client.post(url + f"/delete/comment/{comment.comment_id}")
    assert r.status_code == 404

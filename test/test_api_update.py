from conftest import url
from fastapi.encoders import jsonable_encoder

from owntwitter.models.exceptions import (
    CommentNotFoundException,
    PostNotFoundException,
    UserNotFoundException,
)
from owntwitter.models.factories import CommentFactory, PostFactory, UserFactory


def test_update_user(client, db_service_dependency_override):
    user = UserFactory.build()
    user_json = jsonable_encoder(user)

    r = client.put(url + f"/update/user", json=user_json)
    assert r.status_code == 202


def test_update_user_not_found(client, db_service_dependency_override):
    user = UserFactory.build()
    user_json = jsonable_encoder(user)

    db_service_dependency_override.update_user.side_effect = UserNotFoundException

    r = client.put(url + f"/update/user", json=user_json)
    assert r.status_code == 404


def test_update_post(client, db_service_dependency_override):
    post = PostFactory.build()
    post_json = jsonable_encoder(post)

    r = client.put(url + f"/update/post", json=post_json)
    assert r.status_code == 202


def test_update_post_user_not_found(client, db_service_dependency_override):
    post = PostFactory.build()
    post_json = jsonable_encoder(post)

    db_service_dependency_override.update_post.side_effect = UserNotFoundException

    r = client.put(url + f"/update/post", json=post_json)
    assert r.status_code == 404


def test_update_post_post_not_found(client, db_service_dependency_override):
    post = PostFactory.build()
    post_json = jsonable_encoder(post)

    db_service_dependency_override.update_post.side_effect = PostNotFoundException

    r = client.put(url + f"/update/post", json=post_json)
    assert r.status_code == 404


def test_update_comment(client, db_service_dependency_override):
    comment = CommentFactory.build()
    comment_json = jsonable_encoder(comment)

    r = client.put(url + f"/update/comment", json=comment_json)
    assert r.status_code == 202


def test_update_comment_user_not_found(client, db_service_dependency_override):
    comment = CommentFactory.build()
    comment_json = jsonable_encoder(comment)

    db_service_dependency_override.update_comment.side_effect = UserNotFoundException

    r = client.put(url + f"/update/comment", json=comment_json)
    assert r.status_code == 404


def test_update_comment_post_not_found(client, db_service_dependency_override):
    comment = CommentFactory.build()
    comment_json = jsonable_encoder(comment)

    db_service_dependency_override.update_comment.side_effect = PostNotFoundException

    r = client.put(url + f"/update/comment", json=comment_json)
    assert r.status_code == 404


def test_update_comment_not_found(client, db_service_dependency_override):
    comment = CommentFactory.build()
    comment_json = jsonable_encoder(comment)

    db_service_dependency_override.update_comment.side_effect = CommentNotFoundException

    r = client.put(url + f"/update/comment", json=comment_json)
    assert r.status_code == 404

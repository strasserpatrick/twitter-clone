from conftest import url
from fastapi.encoders import jsonable_encoder
from pymongo.errors import DuplicateKeyError

from owntwitter.models.exceptions import PostNotFoundException, UserNotFoundException
from owntwitter.models.factories import CommentFactory, PostFactory, UserFactory


def test_create_user(client, db_service_dependency_override):
    user = UserFactory.build()
    user_json = jsonable_encoder(user)

    r = client.post(url + f"/create/user", json=user_json)
    assert r.status_code == 201


def test_create_user_exists(client, db_service_dependency_override):
    db_service_dependency_override.create_new_user.side_effect = DuplicateKeyError(
        "error"
    )

    user = UserFactory.build()
    user_json = jsonable_encoder(user)

    r = client.post(url + f"/create/user", json=user_json)
    assert r.status_code == 404


def test_create_post(client, db_service_dependency_override):

    post = PostFactory.build()
    post_json = jsonable_encoder(post)

    r = client.post(url + f"/create/post", json=post_json)
    assert r.status_code == 201


def test_create_post_duplicate(client, db_service_dependency_override):
    db_service_dependency_override.create_new_post.side_effect = DuplicateKeyError(
        "error"
    )

    post = PostFactory.build()
    post_json = jsonable_encoder(post)

    r = client.post(url + f"/create/post", json=post_json)
    assert r.status_code == 404


def test_create_post_user_not_found(client, db_service_dependency_override):
    db_service_dependency_override.create_new_post.side_effect = UserNotFoundException

    post = PostFactory.build()
    post_json = jsonable_encoder(post)

    r = client.post(url + f"/create/post", json=post_json)
    assert r.status_code == 404


def test_create_comment(client, db_service_dependency_override):
    comment = CommentFactory.build()
    comment_json = jsonable_encoder(comment)

    r = client.post(url + f"/create/comment", json=comment_json)
    assert r.status_code == 201


def test_create_comment_user_not_found(client, db_service_dependency_override):
    db_service_dependency_override.create_new_comment.side_effect = (
        UserNotFoundException
    )

    comment = CommentFactory.build()
    comment_json = jsonable_encoder(comment)

    r = client.post(url + f"/create/comment", json=comment_json)
    assert r.status_code == 404


def test_create_comment_post_not_found(client, db_service_dependency_override):
    db_service_dependency_override.create_new_comment.side_effect = (
        PostNotFoundException
    )

    comment = CommentFactory.build()
    comment_json = jsonable_encoder(comment)

    r = client.post(url + f"/create/comment", json=comment_json)
    assert r.status_code == 404

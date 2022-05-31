from fastapi.encoders import jsonable_encoder
from pymongo.errors import DuplicateKeyError

from conftest import url
from owntwitter.models.exceptions import UserNotFoundException
from owntwitter.models.factories import UserFactory, PostFactory


def test_create_user(client, db_service_dependency_override):
    user = UserFactory.build()
    user_json = jsonable_encoder(user)

    r = client.post(url + f"/create/user", json=user_json)
    assert r.status_code == 201


def test_create_user_exists(client, db_service_dependency_override):
    db_service_dependency_override.create_new_user.side_effect = DuplicateKeyError("error")

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
    db_service_dependency_override.create_new_post.side_effect = DuplicateKeyError("error")

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

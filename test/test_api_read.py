from conftest import url

from owntwitter.models.exceptions import PostNotFoundException, UserNotFoundException
from owntwitter.models.factories import CommentFactory, PostFactory, UserFactory


def test_feed_endpoint(client, db_service_dependency_override):
    db_service_dependency_override.read_recent_posts.return_value = PostFactory.batch(
        20
    )

    r = client.get(url + "/feed")

    assert r.status_code == 200
    assert len(r.json()) == 20


def test_get_post(client, db_service_dependency_override):
    post = PostFactory.build()
    db_service_dependency_override.read_post.return_value = post

    r = client.get(url + f"/posts/{post.post_id}")

    assert r.status_code == 200


def test_get_post_not_in_db(client, db_service_dependency_override):
    post = PostFactory.build()
    db_service_dependency_override.read_post.side_effect = PostNotFoundException

    r = client.get(url + f"/posts/{post.post_id}")

    assert r.status_code == 404


def test_get_user(client, db_service_dependency_override):
    user = UserFactory.build()
    db_service_dependency_override.read_user.return_value = user

    r = client.get(url + f"/users/{user.username}")
    assert r.status_code == 200


def test_get_user_not_in_db(client, db_service_dependency_override):
    user = UserFactory.build()
    db_service_dependency_override.read_user.side_effect = UserNotFoundException

    r = client.get(url + f"/users/{user.username}")
    assert r.status_code == 404


def test_get_user_posts(client, db_service_dependency_override):
    user = UserFactory.build()

    posts = PostFactory.batch(10)
    for p in posts:
        p.username = user.username

    db_service_dependency_override.read_posts_of_user.return_value = posts

    r = client.get(url + f"/users/{user.username}/posts")
    assert r.status_code == 200
    assert len(r.json()) == 10


def test_get_users_posts_no_posts(client, db_service_dependency_override):
    user = UserFactory.build()
    db_service_dependency_override.read_posts_of_user.side_effect = (
        UserNotFoundException
    )

    r = client.get(url + f"/users/{user.username}/posts")
    assert r.status_code == 404


def test_get_comments_of_post(client, db_service_dependency_override):
    post = PostFactory.build()

    comments = CommentFactory.batch(10)
    for c in comments:
        c.post_id = post.post_id

    db_service_dependency_override.read_comments_of_post.return_value = comments

    r = client.get(url + f"/posts/{post.post_id}/comments")
    assert r.status_code == 200
    assert len(r.json()) == 10


def test_get_comments_of_post_not_found(client, db_service_dependency_override):
    post = PostFactory.build()
    db_service_dependency_override.read_comments_of_post.side_effect = (
        PostNotFoundException
    )

    r = client.get(url + f"/posts/{post.post_id}/comments")
    assert r.status_code == 404


def test_get_users_of_likes(client, db_service_dependency_override):
    post = PostFactory.build()
    liked_usernames = [u.username for u in UserFactory.batch(10)]
    post.likes = liked_usernames

    db_service_dependency_override.read_post.return_value = post
    db_service_dependency_override.read_user.return_value = UserFactory.build()

    r = client.get(url + f"/posts/{post.post_id}/likes")
    assert r.status_code == 200
    assert len(r.json()) == 10


def test_get_users_of_likes_post_not_found(client, db_service_dependency_override):
    post = PostFactory.build()
    db_service_dependency_override.read_post.side_effect = PostNotFoundException

    r = client.get(url + f"/posts/{post.post_id}/likes")
    assert r.status_code == 404
    assert r.json()["detail"] == "Post not found"


def test_get_users_of_likes_user_not_found(client, db_service_dependency_override):
    post = PostFactory.build()
    db_service_dependency_override.read_post.side_effect = UserNotFoundException

    r = client.get(url + f"/posts/{post.post_id}/likes")
    assert r.status_code == 404
    assert r.json()["detail"] == "User not found"

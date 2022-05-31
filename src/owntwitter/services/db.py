from typing import List

from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient

from owntwitter.models.exceptions import (
    CommentNotFoundException,
    PostNotFoundException,
    UserNotFoundException,
)
from owntwitter.models.models import Comment, Post, User
from owntwitter.models.settings import Settings


class DatabaseConnector:
    def __init__(self):
        settings = Settings()

        self._client = MongoClient(
            f"mongodb://{settings.mongo_db_url}:{settings.mongo_db_port}"
        )

        # Database
        self._db = self._client.twitter

        # Collections
        self._users = self._db.users
        self._posts = self._db.posts
        self._comments = self._db.comments

    # =====================# USERS #=====================#

    def create_new_user(self, user: User):
        # raises duplicate key error, if user already in database
        user_json = jsonable_encoder(user)
        response = self._users.insert_one(user_json)
        return response

    def read_user(self, username: str):
        # read without password, more inheritance user models (personalview and publicview)
        user = self._users.find_one({"_id": username})

        if user is None:
            raise UserNotFoundException()

        pydantic_user = User(
            username=user["_id"], email=user["email"], password=user["password"]
        )

        return pydantic_user

    def update_user(self, new_user):

        return self._users.replace_one(
            {"_id": new_user.username}, jsonable_encoder(new_user)
        )

    def delete_user(self, username):

        # trigger to delete all posts of user
        posts = self.read_posts_of_user(username)

        for p in posts:
            self._posts.delete_one({"_id": p.post_id})

        # trigger to delete all comments of user
        comments = self.read_comments_of_user(username)

        for c in comments:
            self._comments.delete_one({"_id": c.comment_id})

        response = self._users.delete_one({"_id": username})

        return response

    # =====================# POSTS #=====================#

    def create_new_post(self, post: Post):

        # check if user in db
        user = self.read_user(post.username)

        post_json = jsonable_encoder(post)
        return self._posts.insert_one(post_json)

    def read_posts_of_user(self, username: str):
        # check if user in db; possibly throws user not found exception
        self.read_user(username)

        all_posts = list(self._posts.find({"username": username}))
        post_list = [
            Post(
                post_id=r["_id"],
                username=r["username"],
                timestamp=r["timestamp"],
                content=r["content"],
                likes=r["likes"],
                number_of_comments=r["number_of_comments"],
            )
            for r in all_posts
        ]
        return post_list

    def read_post(self, post_id: str):
        post = self._posts.find_one({"_id": post_id})

        if post is None:
            raise PostNotFoundException()

        pydantic_post = Post(
            post_id=post["_id"],
            username=post["username"],
            timestamp=post["timestamp"],
            content=post["content"],
            likes=post["likes"],
            number_of_comments=post["number_of_comments"],
        )

        return pydantic_post

    def read_recent_posts(self, count=10) -> List[Post]:
        posts = list(self._posts.find().sort("timestamp", -1).limit(count))
        if not posts:
            raise PostNotFoundException()

        pydantic_posts = [
            Post(
                post_id=post["_id"],
                username=post["username"],
                timestamp=post["timestamp"],
                content=post["content"],
                likes=post["likes"],
                number_of_comments=post["number_of_comments"],
            )
            for post in posts
        ]

        return pydantic_posts

        # https://stackoverflow.com/questions/24501756/sort-mongodb-documents-by-timestamp-in-desc-order

    def update_post(self, new_post):
        # verify that username does not change
        return self._posts.replace_one(
            {"_id": new_post.post_id}, jsonable_encoder(new_post)
        )

    def delete_post(self, post_id):
        response = self._posts.delete_one({"_id": post_id})

        # trigger to delete all comments of post
        comments = self.read_comments_of_post(post_id)

        for c in comments:
            self._comments.delete_one({"_id": c.comment_id})

        return response

    # =====================# COMMENTS #=====================#

    def create_new_comment(self, comment: Comment):
        # add that post and user must exist

        # check if user in db
        self.read_user(comment.username)
        self.read_post(comment.post_id)

        comment_json = jsonable_encoder(comment)
        return self._comments.insert_one(comment_json)

    def read_comment(self, comment_id: str):
        response = list(self._comments.find({"_id": comment_id}))

        if not response:
            raise CommentNotFoundException()

        r = response.pop()

        return Comment(
            comment_id=r["_id"],
            post_id=r["post_id"],
            username=r["username"],
            timestamp=r["timestamp"],
            content=r["content"],
        )

    def read_comments_of_post(self, post_id: str):
        # check if post exists; possibly throws post_not_found exception
        self.read_post(post_id)

        response = list(self._comments.find({"post_id": post_id}))
        comment_list = [
            Comment(
                comment_id=r["_id"],
                post_id=r["post_id"],
                username=r["username"],
                timestamp=r["timestamp"],
                content=r["content"],
            )
            for r in response
        ]
        return comment_list

    def read_comments_of_user(self, username: str):
        response = list(self._comments.find({"username": username}))

        comment_list = [
            Comment(
                comment_id=r["_id"],
                post_id=r["post_id"],
                username=r["username"],
                timestamp=r["timestamp"],
                content=r["content"],
            )
            for r in response
        ]

        return comment_list

    def update_comment(self, new_comment):
        return self._comments.replace_one(
            {"_id": new_comment.comment_id}, jsonable_encoder(new_comment)
        )

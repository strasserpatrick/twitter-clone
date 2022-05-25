from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient

from owntwitter.models.exceptions import UserNotFoundException
from owntwitter.models.models import User
from owntwitter.models.settings import Settings

if __name__ == "__main__":
    settings = Settings()
    client = MongoClient(f"{settings.mongo_db_url}:{settings.mongo_db_port}")
    db = client.twitter


class DatabaseConnector:
    def __init__(self):
        settings = Settings()

        self._client = MongoClient(f"mongodb://{settings.mongo_db_url}:{settings.mongo_db_port}")

        # Database
        self._db = self._client.twitter

        # Collections
        self._users = self._db.users
        self._posts = self._db.posts
        self._comments = self._db.comments

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

        pydantic_user = User(username=user['_id'], email=user['email'], password=user['password'])

        return pydantic_user

    def update_user(self, new_user):

        return self._users.replace_one(
            {"_id": new_user.username},
            jsonable_encoder(new_user)
        )

    def delete_user(self, username):
        response = self._users.delete_one({"username": username})
        return response

from pydantic_factories import ModelFactory

from owntwitter.models.models import Comment, Post, User


class UserFactory(ModelFactory):
    __model__ = User


class PostFactory(ModelFactory):
    __model__ = Post


class CommentFactory(ModelFactory):
    __model__ = Comment

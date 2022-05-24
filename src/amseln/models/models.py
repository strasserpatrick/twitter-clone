import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, constr

from src.amseln.app import MAX_COMMENT_LENGTH, MAX_CONTENT_LENGTH


class User(BaseModel):
    username: str
    email: EmailStr
    password: str


class Post(BaseModel):
    post_id: str
    timestamp: datetime
    content: Optional[constr(max_length=MAX_CONTENT_LENGTH)]
    likes: List[User.username]
    number_of_comments: int


class Comment(BaseModel):
    comment_id: str
    timestamp: datetime
    post_id: Post.post_id
    username: User.username
    content: Optional[constr(max_length=MAX_COMMENT_LENGTH)]

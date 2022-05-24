import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, constr

from amseln.models.settings import Settings

settings = Settings()


class User(BaseModel):
    username: str
    email: EmailStr
    password: str


class Post(BaseModel):
    post_id: str
    timestamp: datetime
    content: Optional[constr(max_length=settings.max_content_length)]
    likes: List[User.username]
    number_of_comments: int


class Comment(BaseModel):
    comment_id: str
    timestamp: datetime
    post_id: Post.post_id
    username: User.username
    content: Optional[constr(max_length=settings.max_comment_length)]

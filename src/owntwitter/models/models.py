from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, constr, Field

from owntwitter.models.settings import Settings

settings = Settings()


class User(BaseModel):
    username: str = Field(alias="_id")
    email: EmailStr
    password: str

    class Config:
        allow_population_by_field_name = True


class Post(BaseModel):
    post_id: str = Field(alias="_id")
    timestamp: datetime
    content: Optional[constr(max_length=settings.max_content_length)]
    likes: List[str]
    number_of_comments: int

    class Config:
        allow_population_by_field_name = True


class Comment(BaseModel):
    comment_id: str = Field(alias="_id")
    timestamp: datetime
    post_id: str
    username: str
    content: Optional[constr(max_length=settings.max_comment_length)]

    class Config:
        allow_population_by_field_name = True

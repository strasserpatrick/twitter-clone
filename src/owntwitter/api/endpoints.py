import functools
from typing import List, Optional

from fastapi import APIRouter, Depends

from owntwitter.models.models import Post, User, Comment
from owntwitter.services.db import DatabaseConnector

router = APIRouter(prefix="/api")


@functools.lru_cache()
def get_db_service():
    return DatabaseConnector()


@router.get("/")
async def read_root():
    return {"Message": "Welcome to the API root endpoint"}


@router.get("/feed", response_model=List[Post])
async def get_recent_posts(db: DatabaseConnector = Depends(get_db_service)):
    return db.read_recent_posts(20)


@router.get("/posts/{post_id}", response_model=Optional[Post])
async def get_post(post_id, db: DatabaseConnector = Depends(get_db_service)):
    return db.read_post(post_id)


@router.get("/users/{username}", response_model=Optional[User])
async def get_user(username, db: DatabaseConnector = Depends(get_db_service)):
    return db.read_user(username)


@router.get("/users/{username}/posts", response_model=List[Post])
async def get_user_posts(username, db: DatabaseConnector = Depends(get_db_service)):
    return db.read_posts_of_user(username)


@router.get("/posts/{post_id}/comments", response_model=List[Comment])
async def get_comments_of_post(post_id, db: DatabaseConnector = Depends(get_db_service)):
    return db.read_comments_of_post(post_id)



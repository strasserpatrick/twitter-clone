import functools
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pymongo.errors import DuplicateKeyError

from owntwitter.models.exceptions import PostNotFoundException, UserNotFoundException
from owntwitter.models.models import Comment, Post, User
from owntwitter.services.db import DatabaseConnector

router = APIRouter(prefix="/api")


def get_db_service():
    return DatabaseConnector()


###### GET REQUESTS ######


@router.get("/")
async def read_root():
    return {"Message": "Welcome to the API root endpoint"}


@router.get("/feed", response_model=List[Post])
async def get_recent_posts(db: DatabaseConnector = Depends(get_db_service)):
    return db.read_recent_posts(20)


@router.get("/posts/{post_id}", response_model=Optional[Post])
async def get_post(post_id, db: DatabaseConnector = Depends(get_db_service)):
    try:
        return db.read_post(post_id)
    except PostNotFoundException:
        raise HTTPException(status_code=404, detail="Post not found")


@router.get("/users/{username}", response_model=Optional[User])
async def get_user(username, db: DatabaseConnector = Depends(get_db_service)):
    try:
        return db.read_user(username)
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/users/{username}/posts", response_model=List[Post])
async def get_user_posts(username, db: DatabaseConnector = Depends(get_db_service)):
    try:
        return db.read_posts_of_user(username)
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/posts/{post_id}/comments", response_model=List[Comment])
async def get_comments_of_post(
        post_id, db: DatabaseConnector = Depends(get_db_service)
):
    try:
        return db.read_comments_of_post(post_id)
    except PostNotFoundException:
        raise HTTPException(status_code=404, detail="Post not found")


@router.get("/posts/{post_id}/likes", response_model=List[User])
async def get_likes_of_post(post_id, db: DatabaseConnector = Depends(get_db_service)):
    try:
        post = db.read_post(post_id)
        usernames_of_likes = post.likes
        return [db.read_user(u) for u in usernames_of_likes]

    except PostNotFoundException:
        raise HTTPException(status_code=404, detail="Post not found")
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")


##### POST REQUESTS #####


@router.post("/create/user", status_code=201)
async def create_user(user: User, db: DatabaseConnector = Depends(get_db_service)):
    try:
        db.create_new_user(user)

    except DuplicateKeyError:
        raise HTTPException(status_code=404, detail="User already exists")


@router.post("/create/post", status_code=201)
async def create_post(post: Post, db: DatabaseConnector = Depends(get_db_service)):
    try:
        db.create_new_post(post)
    except DuplicateKeyError:
        raise HTTPException(status_code=404, detail="Post already exists")
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/create/comment", status_code=201)
async def create_comment(comment: Comment, db: DatabaseConnector = Depends(get_db_service)):
    try:
        db.create_new_comment(comment)
    except DuplicateKeyError:
        raise HTTPException(status_code=404, detail="Comment already exists")
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except PostNotFoundException:
        raise HTTPException(status_code=404, detail="Post not found")

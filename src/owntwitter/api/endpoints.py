import functools
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pymongo.errors import DuplicateKeyError

from owntwitter.models.exceptions import (
    CommentNotFoundException,
    PostNotFoundException,
    UserNotFoundException,
)
from owntwitter.models.models import Comment, Post, User
from owntwitter.services.db import DatabaseConnector

router = APIRouter(prefix="/api")


def get_db_service():
    return DatabaseConnector()


###### READ ######


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


##### CREATE #####


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
async def create_comment(
    comment: Comment, db: DatabaseConnector = Depends(get_db_service)
):
    try:
        db.create_new_comment(comment)
    except DuplicateKeyError:
        raise HTTPException(status_code=404, detail="Comment already exists")
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except PostNotFoundException:
        raise HTTPException(status_code=404, detail="Post not found")


##### UPDATE ENDPOINTS ######


@router.put("/update/user", status_code=202)
async def update_user(new_user: User, db: DatabaseConnector = Depends(get_db_service)):
    try:
        db.update_user(new_user)
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/update/post", status_code=202)
async def update_post(new_post: Post, db: DatabaseConnector = Depends(get_db_service)):
    try:
        db.update_post(new_post)
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except PostNotFoundException:
        raise HTTPException(status_code=404, detail="Post not found")


@router.put("/update/comment", status_code=202)
async def update_comment(
    new_comment: Comment, db: DatabaseConnector = Depends(get_db_service)
):
    try:
        db.update_comment(new_comment)
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except PostNotFoundException:
        raise HTTPException(status_code=404, detail="Post not found")
    except CommentNotFoundException:
        raise HTTPException(status_code=404, detail="Comment not found")


##### DELETE ENDPOINTS #####


@router.post("/delete/user/{username}", status_code=203)
async def delete_user(username: str, db: DatabaseConnector = Depends(get_db_service)):
    try:
        db.delete_user(username)
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/delete/post/{post_id}", status_code=203)
async def delete_post(post_id: str, db: DatabaseConnector = Depends(get_db_service)):
    try:
        db.delete_post(post_id)
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except PostNotFoundException:
        raise HTTPException(status_code=404, detail="Post not found")


@router.post("/delete/comment/{comment_id}", status_code=203)
async def delete_comment(
    comment_id: str, db: DatabaseConnector = Depends(get_db_service)
):
    try:
        db.delete_comment(comment_id)
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except PostNotFoundException:
        raise HTTPException(status_code=404, detail="Post not found")
    except CommentNotFoundException:
        raise HTTPException(status_code=404, detail="Comment not found")

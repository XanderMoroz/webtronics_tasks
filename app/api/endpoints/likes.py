from app.api.schemas.posts import PostDetailsModel, PostModel
from app.api.schemas.users import User
from app.db.cruds import posts as post_utils
from app.db.cruds import likes as like_utils
from app.api.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status

likes_router = APIRouter()


@likes_router.post("/like/{post_id}")
async def add_post_like(post_id: int, current_user=Depends(get_current_user)):
    """**Get recipe by id** / Получить рецепт по идентификатору"""
    post = await post_utils.get_post(post_id)
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no post in the database. Try another one",
        )
    if post["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to like your own post.",
        )
    new_like = await like_utils.add_like(post_id, current_user)

    return {"response": "Like successfully added",
            "post_title": post["title"],
            "like_author": new_like["like_author"]}

@likes_router.delete("/like/{post_id}")
async def remove_post_like(post_id: int, current_user=Depends(get_current_user)):
    """**Get recipe by id** / Получить рецепт по идентификатору"""
    post = await post_utils.get_post(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no post in the database. Try another one",
        )
    like = await like_utils.get_like(post_id)
    if like is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Like already removed.",
        )
    await like_utils.delete_like(like["id"])
    return {"response": "Like successfully deleted",
            "post_title": post["title"],
            "like_author": current_user["name"]}

@likes_router.post("/dislike/{post_id}")
async def add_post_dislike(post_id: int, current_user=Depends(get_current_user)):
    """**Get recipe by id** / Получить рецепт по идентификатору"""
    post = await post_utils.get_post(post_id)
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no post in the database. Try another one",
        )
    if post["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to like your own post.",
        )
    new_dislike = await like_utils.add_dislike(post_id, current_user)

    return {"response": "Like successfully added",
            "post_title": post["title"],
            "dislike_author": new_dislike["dislike_author"]}

@likes_router.delete("/dislike/{post_id}")
async def remove_post_dislike(post_id: int, current_user=Depends(get_current_user)):
    """**Get recipe by id** / Получить рецепт по идентификатору"""
    post = await post_utils.get_post(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no post in the database. Try another one",
        )
    dislike = await like_utils.get_dislike(post_id)
    if dislike is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dislike already removed.",
        )
    await like_utils.delete_dislike(dislike["id"])
    return {"response": "Dislike successfully deleted",
            "post_title": post["title"],
            "dislike_author": current_user["name"]}
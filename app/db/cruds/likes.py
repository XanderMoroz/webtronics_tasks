from datetime import datetime

from app.core.database import database
from app.db.models.posts import posts_table
from app.db.models.users import users_table
from app.db.models.likes import likes_table, dislikes_table
from app.api.schemas import posts as post_schema
from sqlalchemy import desc, func, select


async def add_like(post_id, user):
    query = (
        likes_table.insert()
        .values(
            user_id=user["user_id"],
            post_id=post_id,
        )
        .returning(
            likes_table.c.id,
            likes_table.c.post_id,
            likes_table.c.user_id,
        )
    )
    new_like = await database.fetch_one(query)

    # Convert to dict and add user_name key to it
    like = dict(zip(new_like, new_like.values()))
    like["like_author"] = user["name"]
    return like

async def get_like(post_id: int):
    query = (
        select(
            [
                likes_table.c.id,
                likes_table.c.user_id,
                likes_table.c.post_id,
                posts_table.c.title.label("post_title"),
            ]
        )
        .select_from(likes_table.join(posts_table))
        .where(posts_table.c.id == post_id)
    )
    return await database.fetch_one(query)

async def delete_like(like_id: int):
    query = (
        likes_table.delete()
        .where(likes_table.c.id == like_id)
    )
    return await database.execute(query)


async def add_dislike(post_id, user):
    query = (
        dislikes_table.insert()
        .values(
            user_id=user["user_id"],
            post_id=post_id,
        )
        .returning(
            dislikes_table.c.id,
            dislikes_table.c.post_id,
            dislikes_table.c.user_id,
        )
    )
    new_dislike = await database.fetch_one(query)

    # Convert to dict and add user_name key to it
    dislike = dict(zip(new_dislike, new_dislike.values()))
    dislike["like_author"] = user["name"]
    return dislike

async def get_dislike(post_id: int):
    query = (
        select(
            [
                dislikes_table.c.id,
                dislikes_table.c.user_id,
                dislikes_table.c.post_id,
                posts_table.c.title.label("post_title"),
            ]
        )
        .select_from(dislikes_table.join(posts_table))
        .where(posts_table.c.id == post_id)
    )
    return await database.fetch_one(query)

async def delete_dislike(dislike_id: int):
    query = (
        dislikes_table.delete()
        .where(dislikes_table.c.id == dislike_id)
    )
    return await database.execute(query)
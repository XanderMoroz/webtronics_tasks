from datetime import datetime

from app.core.database import database
from app.db.models.posts import posts_table
from app.db.models.users import users_table
from app.api.schemas import posts as post_schema
from sqlalchemy import desc, func, select


async def create_post(post: post_schema.PostModel, user):
    query = (
        posts_table.insert()
        .values(
            title=post.title,
            content=post.content,
            created_at=datetime.now(),
            user_id=user["user_id"],
        )
        .returning(
            posts_table.c.id,
            posts_table.c.title,
            posts_table.c.content,
            posts_table.c.created_at,
        )
    )
    new_post = await database.fetch_one(query)

    # Convert to dict and add user_name key to it
    recipe = dict(zip(new_post, new_post.values()))
    recipe["user_name"] = user["name"]
    return recipe


async def get_post(post_id: int):
    query = (
        select(
            [
                posts_table.c.id,
                posts_table.c.created_at,
                posts_table.c.title,
                posts_table.c.content,
                posts_table.c.user_id,
                users_table.c.name.label("user_name"),
            ]
        )
        .select_from(posts_table.join(users_table))
        .where(posts_table.c.id == post_id)
    )
    return await database.fetch_one(query)


async def get_posts(page: int):
    max_per_page = 10
    offset1 = (page - 1) * max_per_page
    query = (
        select(
            [
                posts_table.c.id,
                posts_table.c.created_at,
                posts_table.c.title,
                posts_table.c.content,
                posts_table.c.user_id,
                users_table.c.name.label("user_name"),
            ]
        )
        .select_from(posts_table.join(users_table))
        .order_by(desc(posts_table.c.created_at))
        .limit(max_per_page)
        .offset(offset1)
    )
    return await database.fetch_all(query)


async def get_posts_count():
    query = select([func.count()]).select_from(posts_table)
    return await database.fetch_val(query)



async def update_post(post_id: int, post: post_schema.PostModel):
    query = (
        posts_table.update()
        .where(posts_table.c.id == post_id)
        .values(title=post.title, content=post.content)
    )
    return await database.execute(query)

async def delete_post(post_id: int):
    query = (
        posts_table.delete()
        .where(posts_table.c.id == post_id)
    )
    return await database.execute(query)

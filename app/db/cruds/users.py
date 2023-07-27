from datetime import datetime, timedelta
from sqlalchemy import and_

from app.core.database import database
from app.core.security import get_random_string, hash_password
from app.db.models.users import tokens_table, users_table
from app.api.schemas import users as user_schema


async def create_user(user: user_schema.UserCreate):
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    query = users_table.insert().values(
        email=user.email,
        name=user.name,
        hashed_password=f"{salt}${hashed_password}"
    )
    user_id = await database.execute(query)
    token = await create_user_token(user_id)
    token_dict = {
        "token": token["token"],
        "expires": token["expires"]
    }

    return {**user.dict(), "id": user_id, "is_active": True, "token": token_dict}


async def create_user_token(user_id: int):
    query = (
        tokens_table.insert()
        .values(expires=datetime.now() + timedelta(weeks=2), user_id=user_id)
        .returning(tokens_table.c.token, tokens_table.c.expires)
    )

    return await database.fetch_one(query)


async def get_user_by_token(token: str):
    query = tokens_table.join(users_table).select().where(
        and_(
            tokens_table.c.token == token,
            tokens_table.c.expires > datetime.now()
        )
    )
    return await database.fetch_one(query)


async def get_user(user_id: int):
    query = users_table.select().where(users_table.c.id == user_id)
    return await database.fetch_one(query)


async def get_user_by_email(email: str):
    query = users_table.select().where(users_table.c.email == email)
    return await database.fetch_one(query)
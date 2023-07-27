from app.api.schemas import users
from app.db.cruds import users as users_utils
from app.core import security as security_utils
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter()


@auth_router.post("/sign-up", response_model=users.User)
async def create_user(user: users.UserCreate):
    """For sign-up fill next fields:
    - **email**: Адрес електронной почты
    - **name**: Имя пользователя
    - **password** Пароль
    """
    db_user = await users_utils.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await users_utils.create_user(user=user)

@auth_router.post("/login", response_model=users.TokenBase)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_utils.get_user_by_email(email=form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not security_utils.validate_password(
        password=form_data.password, hashed_password=user["hashed_password"]
    ):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return await users_utils.create_user_token(user_id=user["id"])


# @auth_router.get("/users/me", response_model=users.UserBase)
# async def get_current_user(current_user: users.User = Depends(get_current_user)):
#     """**Get current user** / Получить текущего пользователя"""
#     return current_user

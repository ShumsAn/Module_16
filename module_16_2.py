from fastapi import FastAPI
from typing import Annotated
from fastapi import Path

app = FastAPI()


@app.get("/")
async def read_root() -> str:
    return 'Главная страница'


@app.get("/user/admin")
async def get_admin() -> str:
    return 'Вы вошли как Администратор'


@app.get("/user/{user_id}")
async def get_user_id(user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", example='50')]) -> str:
    return f'Вы вошли как пользователь № {user_id}'


@app.get("/user/{username}/{age}")
async def get_user(
        username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=120, description="Enter age", example='24')]) -> str:
    return f'Информация о пользователе. Имя: {username}, Возраст: {age}.'

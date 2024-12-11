from fastapi import FastAPI,Path
from typing import Annotated
from fastapi import HTTPException

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}

@app.get("/")
async def get_tasks() -> str:
    return 'Привет'

@app.get("/users")
async def get_tasks():
    return users


@app.post('/user/{username}/{age}')
async def create_user(
        username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=120, description="Enter age", example='24')]) -> str:
    new_id = str(max(int(user_id) for i, user_id in enumerate(users)) + 1)
    users[new_id] = f' Имя: {username}, возраст: {age}'
    return f" User {new_id} is registered"


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
        user_id: str,
        username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=120, description="Enter age", example='24')])-> str:
    for key,value in users.items():
        if key == user_id:
            users[key] = f' Имя: {username}, возраст: {age}'
            return f'The user {user_id} is updated'
    raise HTTPException(status_code=404, detail="User не найден")


@app.delete('/user/{user_id}')
async def del_user(user_id: str) -> str:
    for key,value in users.items():
        if key == user_id:
            del users[key]
            return f' User {user_id} удален '
    raise HTTPException(status_code=404, detail="User не найден")











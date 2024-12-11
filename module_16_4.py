from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel

app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


Users: List[User] = [
    User(id=1, username="Vasya", age=20),
    User(id="2", username="Vasya", age="20")
]


@app.get("/")
async def get_a() -> str:
    return 'Привет'


@app.get("/users", response_model=List[User])
async def get_users():
    return users


@app.post('/user/{username}/{age}', response_model=User)
async def create_user(username: User, age: User):
    new_id = max((i.id for i in users), default=0) + 1
    new_user = User(id=new_id, username=username.username, age=age.age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def update_user(user_id: int, username: User, age: User):
    for user in users:
        if user.id == user_id:
            user.username = username.username
            user.age = age.age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{user_id}', response_model=dict)
async def del_user(user_id: int) -> str:
    for i, user in enumerate(users):
        if user.id == user_id:
            del users[i]
            return f' User {user_id} удален '
    raise HTTPException(status_code=404, detail="User was not found")

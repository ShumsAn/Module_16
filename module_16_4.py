from fastapi import FastAPI, HTTPException, Path
from typing import List, Annotated
from pydantic import BaseModel, Field

app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


Users: List[User] = [
    User(id=1, username="Vasya", age=20)
]


@app.get("/")
async def get_a() -> str:
    return 'Привет'


@app.get("/users", response_model=List[User])
async def get_users():
    return users


"""Попытки сделать ограничения в Классе BaseModel"""
# class UserCreate(BaseModel):
#     username: str = Field(..., min_length=5,
#                                   max_length=15,
#                                   description="Enter username")
#
#     age: int = Field(ge=18, le=120, description="Enter age")


@app.post('/user/{username}/{age}', response_model=User)
# async def create_user(username: UserCreate, age: int): # Попытка воспользоваться классом BaseModel
async def create_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age')]) -> User:
    new_id = (max(i.id for i in users) + 1) if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}', response_model=User)
# async def update_user(user_id: int, username: UserCreate, age: UserCreate): # Попытка воспользоваться классом BaseModel
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')],
                      username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age')]) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{user_id}', response_model=dict)
async def delite_user(user_id: int) -> str:
    for i, user in enumerate(users):
        if user.id == user_id:
            return users.pop(i)
    raise HTTPException(status_code=404, detail="User was not found")

from fastapi import FastAPI, Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel,Field
from fastapi.templating import Jinja2Templates
from typing import Annotated, List


app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)
templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    id: int = Field(ge=1)
    username: str = Field(..., min_length=5,
                                max_length=15,
                                 description="Enter username")

    age: int = Field(ge=18, le=120, description="Enter age")


users: List[User] = [
    User(id=1, username="Vasya", age=20),
    User(id=2, username="Petya", age="25"),
    User(id=3,username = 'UrbanUser', age = 24),
    User(id=4,username='UrbanTest', age= 22),
    User(id=5,username= 'Capybara', age=60)
]


@app.get("/",response_class=HTMLResponse)
async def get_a(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "user": users})


@app.get("/user/{user_id}'", response_class=HTMLResponse)
async def get_users(request: Request, user_id: User.id) -> HTMLResponse:
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User was not found")

@app.post('/user/{username}/{age}')
async def post_user(username: User.username,
                    age: User.age) -> User:
    user_id = max(users, key=lambda x: int(x.id)).id + 1 if users else 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
        user_id: User.id,
        username: User.username,
        age: User.age) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='User was not found')
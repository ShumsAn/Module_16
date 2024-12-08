from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root() -> str:
    return 'Главная страница'


@app.get("/user/admin")
async def get_admin() -> str:
    return 'Вы вошли как Администратор'


@app.get("/user/{user_id}")
async def get_user_id(user_id: int) -> str:
    return f'Вы вошли как пользователь № {user_id}'


@app.get("/user")
async def get_user(username: str, age: int) -> str:
    return f'Информация о пользователе. Имя: {username}, Возраст: {age}.'

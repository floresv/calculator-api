from pydantic import BaseModel, validator
from .....models.user import User


class UserRegister(BaseModel):
    username: str
    password: str
    status: str
    active = False

    @validator('username')
    def validate_username(cls, username):
        if User.exists(User.username == username):
            raise ValueError('username already exists')
        return username


class UserLogin(BaseModel):
    password: str

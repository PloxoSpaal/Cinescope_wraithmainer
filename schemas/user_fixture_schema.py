from pydantic import BaseModel, Field, field_validator

from schemas.auth_shema import LoginRequestSchema
from utils.data_generator import DataGenerator as DG
from typing import List, Optional
from constants import Roles
import datetime


class UserSchema(BaseModel):
    """
    Описание структуры тела запроса для регистрации пользователя
    """
    email: str = Field(default_factory=DG.generate_random_email)
    fullName: str = Field(default_factory=DG.generate_random_name)
    password: str = Field(default_factory=DG.generate_random_password, min_length=8)
    passwordRepeat: str
    roles: List[Roles] = Field(default=Roles.USER)
    banned: Optional[bool] = None
    verified: Optional[bool] = None

    @field_validator('email')
    def check_for_symbol(cls, value: str) -> str:
        if '@' not in value:
            raise ValueError('Email без @')
        return value

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value


class RegisterUserResponseSchema(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    verified: bool
    banned: bool
    roles: List[Roles]
    createdAt: str

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value


class UserFixtureSchema(BaseModel):
    request: UserSchema
    response: RegisterUserResponseSchema

    @property
    def id(self):
        return self.response.id

    @property
    def email(self):
        return self.request.email

    @property
    def password(self):
        return self.request.password

    @property
    def creds(self):
        return LoginRequestSchema(email=self.email, password=self.password)

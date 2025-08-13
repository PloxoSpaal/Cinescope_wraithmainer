from pydantic import BaseModel, Field, field_validator
from typing import List
from constants import Roles


class LoginRequestSchema(BaseModel):
    """
    Описание структуры тела запроса для логина пользователя
    """
    email: str
    password: str


class LoginResponseUserSchema(BaseModel):
    """
    Описание структуры пользователя в ответе логина пользователя
    """
    id: str
    email: str
    fullName: str
    roles: List[Roles]


class LoginResponseSchema(BaseModel):
    """
    Описание структуры тела запроса для регистрации пользователя
    """
    user: LoginResponseUserSchema
    accessToken: str
    refreshToken: str
    expiresIn: int

    @property
    def email(self):
        return self.user.email

    @property
    def id(self):
        return self.user.id


class RefreshTokenResponseSchema(BaseModel):
    """
    Описание структуры ответа рефреша токенов
    """
    accessToken: str
    refreshToken: str
    expriesIn: int


class RegisterRequestSchema(BaseModel):
    """
    Описание структуры тела запроса метода регистрации
    """
    email: str
    fullName: str
    password: str
    passwordRepeat: str


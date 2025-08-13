from pydantic import BaseModel
from typing import List, Optional
from constants import Roles


class GetUserResponseSchema(BaseModel):
    id: str
    email: str
    fullName: str
    roles: List[Roles]
    verified: bool
    createdAt: str
    banned: bool


class UpdateUserRequestSchema(BaseModel):
    roles: Optional[List[Roles]]
    verified: Optional[bool]
    banned: Optional[bool]


class CreateUserRequestSchema(BaseModel):
    fullName: str
    email: str
    password: str
    verified: bool
    banned: bool


class GetUserListSchema(BaseModel):
    users: List[GetUserResponseSchema]
    count: int
    page: int
    pageSize: int


class DeleteUserResponseSchema(GetUserResponseSchema):
    pass


class UpdateUserResponseSchema(GetUserResponseSchema):
    pass


class CreateUserResponseSchema(GetUserResponseSchema):
    pass

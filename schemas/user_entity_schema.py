from pydantic import BaseModel
from typing import List, Any
from constants import Roles


class User(BaseModel):
    email: str
    password: str
    roles: List[Roles]
    api: Any
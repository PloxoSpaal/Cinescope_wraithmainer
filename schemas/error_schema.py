from pydantic import BaseModel


class BaseError(BaseModel):
    message: str
    statusCode: int
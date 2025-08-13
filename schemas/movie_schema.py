from pydantic import BaseModel, HttpUrl, field_validator
from typing import List, Dict,Optional


class CreateMovieRequestSchema(BaseModel):
    name: str
    imageUrl: Optional[str]
    price: int
    description: str
    location: str
    published: bool
    genreId: int


class GenreNameSchema(BaseModel):
    name: str


class GetMoviesResponseMovieSchema(CreateMovieRequestSchema):
    id: int
    genre: GenreNameSchema
    createdAt: str
    rating: float


class GetMoviesResponseSchema(BaseModel):
    movies: List[GetMoviesResponseMovieSchema]
    count: int
    page: int
    pageSize: int
    pageCount: int


class FullNameSchema(BaseModel):
    fullName: str


class ReviewSchema(BaseModel):
    userId: str
    rating: int
    text: str
    hidden: bool
    createdAt: str
    user: FullNameSchema


class GetMovieResponseSchema(GetMoviesResponseMovieSchema):
    reviews: List[ReviewSchema]


class UpdateMovieRequestSchema(BaseModel):
    name: Optional[str]
    imageUrl: Optional[HttpUrl]
    price: Optional[int]
    description: Optional[str]
    location: Optional[str]
    published: Optional[bool]
    genreId: Optional[int]


class CreateMovieResponseSchema(GetMoviesResponseMovieSchema):
    pass


class DeleteMovieResponseSchema(GetMoviesResponseMovieSchema):
    pass


class UpdateMovieResponseSchema(GetMoviesResponseMovieSchema):
    pass
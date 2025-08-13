from pydantic import BaseModel, Field, field_validator
from schemas.movie_schema import CreateMovieRequestSchema, CreateMovieResponseSchema


class MovieFixtureSchema(BaseModel):
    request: CreateMovieRequestSchema
    response: CreateMovieResponseSchema

    @property
    def id(self):
        return self.response.id

    @property
    def name(self):
        return self.request.name

    @property
    def price(self):
        return self.request.price

    @property
    def description(self):
        return self.request.description

    @property
    def image_url(self):
        return self.request.imageUrl

    @property
    def location(self):
        return self.request.location

    @property
    def published(self):
        return self.request.published

    @property
    def rating(self):
        return self.response.rating

    @property
    def genre_id(self):
        return self.response.genreId

    @property
    def created_at(self):
        return self.response.createdAt
from pydantic import BaseModel, Field


class MovieBaseSchema(BaseModel):
    name: str = Field(..., max_length=100)


class MovieCreateSchema(MovieBaseSchema):
    pass


class MovieUpdateSchema(MovieBaseSchema):
    pass


class MovieResponseSchema(MovieBaseSchema):
    id: int

    model_config = {
        "from_attributes": True
    }


class FavoriteMovieSchema(BaseModel):
    movie_id: int
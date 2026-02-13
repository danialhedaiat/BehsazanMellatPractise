from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from movie.models import MoviesModel
from movie.schemas import MovieResponseSchema, MovieCreateSchema, MovieUpdateSchema

router = APIRouter(tags=["Movies"], prefix="/movies")

@router.get("/", response_model=List[MovieResponseSchema])
async def retrive_movie_list(db: Session = Depends(get_db)):
    movies = db.query(MoviesModel).all()
    return movies


@router.get("/{movie_id}", response_model=MovieResponseSchema)
async def retrive_movie_detail(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MoviesModel).filter_by(id=movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/", response_model=MovieResponseSchema)
async def create_movie(request_movie: MovieCreateSchema, db: Session = Depends(get_db)):
    movie = MoviesModel(**request_movie.model_dump())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


@router.put("/{movie_id}", response_model=MovieResponseSchema)
async def update_movie(request_movie: MovieUpdateSchema,movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MoviesModel).filter_by(id=movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = request_movie.model_dump()

    for key, value in update_data.items():
        setattr(movie, key, value)

    db.commit()
    db.refresh(movie)
    return movie


@router.delete("/{movie_id}", status_code=204)
async def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MoviesModel).filter_by(id=movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    db.delete(movie)
    db.commit()


@router.post('/favorite')
async def add_favorite_movie(db: Session = Depends(get_db)):
    pass

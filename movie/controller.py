from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.auth import get_current_user
from core.database import get_db
from movie.models import MoviesModel, UserFavoriteMovieModel
from movie.schemas import MovieResponseSchema, MovieCreateSchema, MovieUpdateSchema, FavoriteMovieSchema
from user.models import UserModel

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
async def update_movie(request_movie: MovieUpdateSchema, movie_id: int, db: Session = Depends(get_db)):
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
async def add_favorite_movie(request_movie: FavoriteMovieSchema, db: Session = Depends(get_db),
                             current_user: UserModel = Depends(get_current_user)):
    movie = db.query(MoviesModel).filter_by(id=request_movie.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    existing = db.query(UserFavoriteMovieModel).filter_by(
        user_id=current_user.id,
        movie_id=request_movie.movie_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Movie already in favorites")

    # Add favorite
    favorite = UserFavoriteMovieModel(user_id=current_user.id, movie_id=request_movie.movie_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return {
        "message": "your favorite movie successfully added",
        "movie": movie.name,
        "user_id": current_user.id,
        "detail": favorite
    }


@router.get('/favorite/')
async def get_favorite_movie(db: Session = Depends(get_db),
                             current_user: UserModel = Depends(get_current_user)
                             ):

    favorites = db.query(UserFavoriteMovieModel).filter_by(user_id=current_user.id).all()

    movie_names = [fav.movie.name for fav in favorites]

    return {"favorite_movies": movie_names}

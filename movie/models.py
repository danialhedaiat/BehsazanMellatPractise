from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from core.database import Base


class MoviesModel(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    favorited_by = relationship(
        "UserFavoriteMovieModel",
        back_populates="movie",
        cascade="all, delete"
    )


class UserFavoriteMovieModel(Base):
    __tablename__ = 'user_favorite_movies'

    __table_args__ = (
        UniqueConstraint('user_id', 'movie_id', name='unique_user_movie'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)

    user = relationship("UserModel", back_populates="favorite_movies")
    movie = relationship("MoviesModel", back_populates="favorited_by")

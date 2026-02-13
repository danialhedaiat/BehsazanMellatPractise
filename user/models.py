from datetime import datetime

from passlib.context import CryptContext
from sqlalchemy import Column, String, Integer, Boolean, DateTime, func, text
from sqlalchemy.orm import relationship

from core.database import Base
from movie.models import UserFavoriteMovieModel


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    phone_number = Column(String(15), nullable=False, unique=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password = Column(String(250), nullable=False)

    is_verify = Column(Boolean, nullable=False, server_default=text("0"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    favorite_movies = relationship(
        UserFavoriteMovieModel,
        back_populates="user",
        cascade="all, delete",
    )

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)

    def set_password(self, plain_password: str) -> None:
        self.password = pwd_context.hash(plain_password)


from sqlalchemy import UniqueConstraint, Column, Integer, String, Date

from core.database import Base


class JobModel(Base):
    __tablename__ = 'jobs'

    __table_args__ = (
        UniqueConstraint('user_id', 'movie_id', name='unique_user_movie'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_name = Column(String(50), nullable=False)
    run_type = Column(String(50), nullable=False)
    run_time = Column(Date, nullable=False)

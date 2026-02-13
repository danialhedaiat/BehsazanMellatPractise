from contextlib import asynccontextmanager

from fastapi import FastAPI

from movie.controller import router as movie_router
from core.controller import router as core_router
from user.controllers import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")

app = FastAPI(
    title="Behsazan Mellat Bank Practise",
    version="0.0.1",
    contact={
        "name": "Danial Hadi",
        "email": "danialhedaiat@gmail.com",
        "phone_number": "09308222060"
    },
    lifespan=lifespan
)



app.include_router(core_router)
app.include_router(movie_router)
app.include_router(user_router)
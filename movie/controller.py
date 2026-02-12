from fastapi import APIRouter

router = APIRouter(tags=["Movies"], prefix="/movies")

@router.get("/")
async def root(request=None):
    return "Greetings!!"
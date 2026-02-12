from fastapi import APIRouter

router = APIRouter(tags=["core"])

@router.get("/")
async def root(request=None):
    return "Greetings!!"
from typing import List

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from user.models import UserModel
from user.schemas import UserResponseSchema, UserCreateSchema, UserUpdateSchema

router = APIRouter(tags=["User"], prefix="/users")


@router.get("/", response_model=List[UserResponseSchema])
async def retrive_user_list(db: Session = Depends(get_db)):
    result = db.query(UserModel).all()
    return result


@router.get("/{user_id}", response_model=UserResponseSchema)
async def retrive_user_detail(user_id: int, db: Session = Depends(get_db)):
    result = db.query(UserModel).filter_by(id=user_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.post("/", response_model=UserResponseSchema)
async def create_user(request_user: UserCreateSchema, db: Session = Depends(get_db)):
    user_obj = UserModel(**request_user.model_dump())
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


@router.put("/{user_id}", response_model=UserResponseSchema)
async def update_user(request_user: UserUpdateSchema,user_id: int, db: Session = Depends(get_db)):
    user  = db.query(UserModel).filter_by(id=user_id).first()
    if not user :
        raise HTTPException(status_code=404, detail="User not found")

    update_data = request_user.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

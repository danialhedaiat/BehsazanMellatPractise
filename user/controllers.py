from typing import List

from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from user.models import UserModel
from user.schemas import UserResponseSchema, UserCreateSchema, UserUpdateSchema, UserLoginSchema

router = APIRouter(tags=["User"], prefix="/users")


@router.get("/", response_model=List[UserResponseSchema])
async def retrive_user_list(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users


@router.get("/{user_id}", response_model=UserResponseSchema)
async def retrive_user_detail(user_id: int, db: Session = Depends(get_db)):
    result = db.query(UserModel).filter_by(id=user_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.post("/", response_model=UserResponseSchema)
async def register_user(request_user: UserCreateSchema, db: Session = Depends(get_db)):
    if db.query(UserModel).filter_by(email=request_user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user_obj = UserModel(email=request_user.email, phone_number=request_user.phone_number,
                         first_name=request_user.first_name, last_name=request_user.last_name)
    user_obj.set_password(request_user.password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


@router.put("/{user_id}", response_model=UserResponseSchema)
async def update_user(request_user: UserUpdateSchema, user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter_by(id=user_id).first()
    if not user:
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


@router.post("/token")
async def get_token(request_login: UserLoginSchema, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter_by(email=request_login.email).first()

    if not user or not user.verify_password(request_login.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token({"user_id": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

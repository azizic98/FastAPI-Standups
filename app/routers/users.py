from typing import List

import models
import oauth2
import schemas
import utils
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])


# Helper functions
def get_user_by_id(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found.",
        )
    return user


# Publicly Accessible Endpoints


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    return get_user_by_id(db, id)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.put(
    "/update/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut
)
def update_user(
    id: int,
    user_data: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    user = get_user_by_id(db, id)

    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You don't have permission to update this user.",
        )

    if user_data.current_password and not utils.verify_password(
        user_data.current_password, user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password.",
        )

    if user_data.email:
        user.email = user_data.email
    if user_data.password:
        user.password = utils.hash_password(user_data.password)

    db.commit()
    db.refresh(user)
    return user


# Admin-Only Endpoints


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut
)
def create_user(
    user: schemas.UserBase,
    db: Session = Depends(get_db),
    is_admin=Depends(oauth2.check_user_authorization),
):
    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    user.password = utils.hash_password(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    is_admin=Depends(oauth2.check_user_authorization),
):
    user = get_user_by_id(db, id)

    db.delete(user)
    db.commit()

    return None

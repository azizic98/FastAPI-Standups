from typing import List

import schemas as schemas
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models import Standup, User
from sqlalchemy import text
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/sql_injections",
    tags=["SQL Injections"],
)


# Endpoint using ORM
@router.get("/orm/{user_id}/")
def get_standups_orm(user_id, db: Session = Depends(get_db)):
    try:
        standups = db.query(Standup).filter(Standup.user_id == user_id).all()
    except DataError:
        error_message = "An error occurred while processing your request."
        return HTTPException(status_code=500, detail=error_message)
    return standups


# Endpoint using Raw SQL (Vulnerable to SQL Injection)
@router.get("/raw/{user_id}/", response_model=List[schemas.StandupResponse])
def get_standups_raw_sql(user_id, db: Session = Depends(get_db)):
    query = text(f"SELECT * FROM standups WHERE user_id = {user_id}")
    standups = db.execute(query).fetchall()
    return standups

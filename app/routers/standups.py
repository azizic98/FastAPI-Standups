from datetime import date, timedelta
from typing import List, Union

from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from models import Standup, User
from oauth2 import get_current_user
from schemas import StandupCreate, StandupListResponse, StandupResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/standups", tags=["Standups"])


@router.post("/create_standup/", response_model=StandupResponse)
def create_standup(
    standup_data: StandupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # If no date is provided , defaults to today , else uses entered date
    standup_date = standup_data.date if standup_data.date else date.today()

    # Prevent users from creating Standups for future dates
    if standup_date > date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create standups for future dates",
        )

    # Cannot create more than one standup for a specific date
    existing_standup = (
        db.query(Standup)
        .filter(Standup.user_id == current_user.id, Standup.date == standup_date)
        .first()
    )

    if existing_standup:
        if standup_data.date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A standup for {standup_date} already exists",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already created a standup today",
            )

    # Create new standup
    new_standup = Standup(
        content=standup_data.content, user_id=current_user.id, date=standup_date
    )

    db.add(new_standup)
    db.commit()
    db.refresh(new_standup)
    return new_standup


@router.get("/by_date/{requested_date}/", response_model=StandupListResponse)
def get_standup_by_date(
    requested_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    standups = (
        db.query(Standup)
        .filter(Standup.user_id == current_user.id, Standup.date == requested_date)
        .all()
    )
    return {"standups": standups}


@router.get("/by_days/{days}/")
def get_standups_by_days(
    days: int,
    v: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    start_date = date.today() - timedelta(days=days)
    standups = (
        db.query(Standup)
        .filter(Standup.user_id == current_user.id, Standup.date >= start_date)
        .all()
    )
    if v:
        standups_content = "\n".join(["- " + s.content for s in standups])
        return PlainTextResponse(content=standups_content)
    return {"Standups": standups}

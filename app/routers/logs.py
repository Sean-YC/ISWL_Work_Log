from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(
    prefix="/logs",
    tags=["logs"]
)

# add a new log
@router.post("/", response_model=schemas.LogResponse)
def create_log(log: schemas.LogCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_log = models.Log(
        user_id=current_user.id,
        date=log.date,
        start_time=log.start_time,  # Required start time ("in")
        working_hours=log.working_hours,
        task_description=log.task_description
        # status and reviewer_id are not required in the form, keep default
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

# get all logs
@router.get("/", response_model=List[schemas.LogResponse])
def get_my_logs(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    logs = db.query(models.Log).filter(models.Log.user_id == current_user.id).all()
    return logs

@router.put("/{log_id}", response_model=schemas.LogResponse)
def update_log(
    log_id: int,
    log_update: schemas.LogUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Get the log
    db_log = db.query(models.Log).filter(models.Log.id == log_id).first()
    if not db_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log not found"
        )

    # Check permissions
    is_owner = db_log.user_id == current_user.id
    is_supervisor = current_user.role in ["supervisor", "admin"]

    if not (is_owner or is_supervisor):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this log"
        )

    # If user is owner, they can't change status or reviewer_id
    if is_owner:
        if log_update.status is not None or log_update.reviewer_id is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Users can't change log status or reviewer"
            )

    # If user is supervisor, they can only change status and reviewer_id
    if is_supervisor:
        update_data = {
            "status": log_update.status,
            "reviewer_id": current_user.id
        }
    else:
        # For owners, update all other fields
        update_data = log_update.dict(exclude_unset=True)
        # Convert date string to date object if present
        if update_data.get('date'):
            update_data['date'] = datetime.strptime(update_data['date'], '%Y-%m-%d').date()

    # Update the log
    for key, value in update_data.items():
        if value is not None:
            setattr(db_log, key, value)

    db.commit()
    db.refresh(db_log)
    return db_log

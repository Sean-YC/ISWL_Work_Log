from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

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
        week_number=log.week_number,
        day=log.day,
        date=log.date,
        working_hours=log.working_hours,
        task_description=log.task_description,
        status=log.status,  # 🔥 pass in the status
        reviewer_id=log.reviewer_id  # 🔥 pass in the reviewer_id
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

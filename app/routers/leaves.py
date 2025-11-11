from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(
    prefix="/leaves",
    tags=["leaves"]
)

# Get leave balance (calculated)
@router.get("/balance", response_model=schemas.LeaveBalanceResponse)
def get_leave_balance(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Get current user's available leave balance (calculated from approved requests)"""
    # Get or create base balance
    balance = db.query(models.LeaveBalance).filter(
        models.LeaveBalance.user_id == current_user.id
    ).first()
    
    # If balance doesn't exist, create one with defaults
    if not balance:
        balance = models.LeaveBalance(
            user_id=current_user.id,
            annual_leave=10,
            sick_leave=5,
            personal_leave=5
        )
        db.add(balance)
        db.commit()
        db.refresh(balance)
    
    # Get all approved leave requests for this user
    approved_leaves = db.query(models.Leave).filter(
        models.Leave.user_id == current_user.id,
        models.Leave.status == "approved"
    ).all()
    
    # Calculate used leave days by type
    used_annual = 0
    used_sick = 0
    used_personal = 0
    
    for leave in approved_leaves:
        days = (leave.end_date - leave.start_date).days + 1
        
        if leave.leave_type == "annual_leave":
            used_annual += days
        elif leave.leave_type == "sick_leave":
            used_sick += days
        elif leave.leave_type == "personal_leave":
            used_personal += days
    
    # Calculate available balance
    available_annual = max(0, balance.annual_leave - used_annual)
    available_sick = max(0, balance.sick_leave - used_sick)
    available_personal = max(0, balance.personal_leave - used_personal)
    
    # Return calculated balance
    return {
        "user_id": balance.user_id,
        "annual_leave": available_annual,
        "sick_leave": available_sick,
        "personal_leave": available_personal
    }

# Create leave request
@router.post("/", response_model=schemas.LeaveResponse)
def create_leave(
    leave: schemas.LeaveCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Create a new leave request"""
    # Validate dates
    if leave.end_date < leave.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date"
        )
    
    # Calculate number of days
    days = (leave.end_date - leave.start_date).days + 1
    
    # Check balance
    balance = db.query(models.LeaveBalance).filter(
        models.LeaveBalance.user_id == current_user.id
    ).first()
    
    if not balance:
        # Create balance if doesn't exist
        balance = models.LeaveBalance(
            user_id=current_user.id,
            annual_leave=10,
            sick_leave=5,
            personal_leave=5
        )
        db.add(balance)
        db.commit()
        db.refresh(balance)
    
    # Check if user has enough leave balance
    leave_type_map = {
        "annual_leave": balance.annual_leave,
        "sick_leave": balance.sick_leave,
        "personal_leave": balance.personal_leave
    }
    
    available_days = leave_type_map.get(leave.leave_type.value, 0)
    if days > available_days:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient leave balance. Available: {available_days} days, Requested: {days} days"
        )
    
    # Create leave request
    db_leave = models.Leave(
        user_id=current_user.id,
        leave_type=leave.leave_type.value,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason,
        contact=leave.contact,
        created_at=date.today()
    )
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave

# Get all leave requests for current user
@router.get("/", response_model=List[schemas.LeaveResponse])
def get_my_leaves(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Get all leave requests for current user"""
    leaves = db.query(models.Leave).filter(
        models.Leave.user_id == current_user.id
    ).order_by(models.Leave.created_at.desc()).all()
    return leaves

# Update leave request
@router.put("/{leave_id}", response_model=schemas.LeaveResponse)
def update_leave(
    leave_id: int,
    leave_update: schemas.LeaveUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Update a leave request"""
    db_leave = db.query(models.Leave).filter(models.Leave.id == leave_id).first()
    if not db_leave:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found"
        )
    
    # Check permissions
    is_owner = db_leave.user_id == current_user.id
    is_supervisor = current_user.role in ["supervisor", "admin"]
    
    if not (is_owner or is_supervisor):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this leave request"
        )
    
    # If user is owner, they can't change status
    if is_owner:
        if leave_update.status is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Users can't change leave request status"
            )
    
    # If user is supervisor, they can only change status and reviewer_id
    if is_supervisor:
        update_data = {
            "status": leave_update.status.value if leave_update.status else None,
            "reviewer_id": current_user.id if leave_update.status else None
        }
    else:
        # For owners, update all other fields
        update_data = leave_update.model_dump(exclude_unset=True, exclude={"status"})
        if "leave_type" in update_data and update_data["leave_type"]:
            update_data["leave_type"] = update_data["leave_type"].value
    
    # Update the leave request
    for key, value in update_data.items():
        if value is not None:
            setattr(db_leave, key, value)
    
    db.commit()
    db.refresh(db_leave)
    return db_leave

# Delete leave request
@router.delete("/{leave_id}", response_model=dict)
def delete_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Delete a leave request"""
    db_leave = db.query(models.Leave).filter(models.Leave.id == leave_id).first()
    if not db_leave:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found"
        )
    
    # Check permissions
    is_owner = db_leave.user_id == current_user.id
    is_supervisor = current_user.role in ["supervisor", "admin"]
    
    if not (is_owner or is_supervisor):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this leave request"
        )
    
    # Only pending requests can be deleted
    if db_leave.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending leave requests can be deleted"
        )
    
    # Delete the leave request
    db.delete(db_leave)
    db.commit()
    
    return {"message": "Leave request deleted successfully", "leave_id": leave_id}


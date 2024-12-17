from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Plan, Permission, Subscription, User
from database import SessionLocal
from schemas import PlanCreate, PlanUpdate, PermissionCreate, PermissionUpdate
from auth import verify_access_token

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Plan
@router.post("/plans")
def create_plan(plan: PlanCreate, db: Session = Depends(get_db)):
    new_plan = Plan(name=plan.name, description=plan.description, api_permissions=plan.api_permissions, limits=plan.limits)
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan

# Modify Plan
@router.put("/plans/{plan_id}")
def update_plan(plan_id: int, plan: PlanUpdate, db: Session = Depends(get_db)):
    db_plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    db_plan.name = plan.name or db_plan.name
    db_plan.description = plan.description or db_plan.description
    db_plan.api_permissions = plan.api_permissions or db_plan.api_permissions
    db_plan.limits = plan.limits or db_plan.limits
    db.commit()
    return db_plan

# Delete Plan
@router.delete("/plans/{plan_id}")
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    db_plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    db.delete(db_plan)
    db.commit()
    return {"message": "Plan deleted"}

# Add Permission
@router.post("/permissions")
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    new_permission = Permission(api_endpoint=permission.api_endpoint, description=permission.description)
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return new_permission

# Modify Permission (PUT)
@router.put("/permissions/{permission_id}")
def update_permission(permission_id: int, permission: PermissionUpdate, db: Session = Depends(get_db)):
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    db_permission.api_endpoint = permission.api_endpoint or db_permission.api_endpoint
    db_permission.description = permission.description or db_permission.description
    db.commit()
    return {"message": "Permission updated successfully", "permission": db_permission}

# Delete Permission (DELETE)
@router.delete("/permissions/{permission_id}")
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    db.delete(db_permission)
    db.commit()
    return {"message": "Permission deleted successfully"}
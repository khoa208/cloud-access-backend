from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Subscription, Plan, Usage
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Check Access and Track Usage
@router.get("/access/{user_id}/{api_endpoint}")
def check_access(user_id: int, api_endpoint: str, db: Session = Depends(get_db)):
    subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="No subscription found")

    plan = db.query(Plan).filter(Plan.id == subscription.plan_id).first()
    if api_endpoint not in plan.api_permissions:
        raise HTTPException(status_code=403, detail="Access Denied")

    # Check Usage
    usage = db.query(Usage).filter_by(user_id=user_id, api_endpoint=api_endpoint).first()
    if usage and usage.request_count >= plan.limits.get(api_endpoint, 0):
        raise HTTPException(status_code=429, detail="API Limit Reached")

    # Update Usage
    if not usage:
        usage = Usage(user_id=user_id, api_endpoint=api_endpoint, request_count=1)
        db.add(usage)
    else:
        usage.request_count += 1
    db.commit()

    return {"message": "Access Granted"}

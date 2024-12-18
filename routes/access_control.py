import json
from fastapi import APIRouter, Depends, HTTPException, Path
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

@router.get("/{user_id}/{api_endpoint:path}")
def check_access(user_id: int,
    api_endpoint: str = Path(..., description="API endpoint", convert_underscores=False),
    db: Session = Depends(get_db),):
    #print(f"Access route hit: user_id={user_id}, api_endpoint={api_endpoint}")
    # Fetch subscription
    subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="No subscription found")

    # Fetch plan details
    plan = db.query(Plan).filter(Plan.id == subscription.plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    # Debug: Check what is returned from plan.api_permissions
    print(f"Plan API Permissions (Raw): {plan.api_permissions}")
    api_permissions = json.loads(plan.api_permissions) if isinstance(plan.api_permissions, str) else plan.api_permissions
    print(f"Parsed API Permissions: {api_permissions}")

    # Check if the endpoint exists in permissions
    if api_endpoint not in api_permissions:
        raise HTTPException(status_code=403, detail="Access Denied: API not permitted")

    # Check usage limits
    limits = json.loads(plan.limits) if isinstance(plan.limits, str) else plan.limits
    usage = db.query(Usage).filter_by(user_id=user_id, api_endpoint=api_endpoint).first()
    if usage and usage.request_count >= limits.get(api_endpoint, 0):
        raise HTTPException(status_code=429, detail="API Limit Reached")

    # Update usage
    if not usage:
        usage = Usage(user_id=user_id, api_endpoint=api_endpoint, request_count=1)
        db.add(usage)
    else:
        usage.request_count += 1
    db.commit()

    return {"message": "Access Granted"}

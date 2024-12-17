from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Subscription, Plan, User, Usage
from database import SessionLocal
from schemas import SubscriptionCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Subscribe to a plan
@router.post("/subscriptions")
def subscribe_to_plan(subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    plan = db.query(Plan).filter(Plan.id == subscription.plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    new_subscription = Subscription(user_id=subscription.user_id, plan_id=subscription.plan_id)
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return new_subscription

# View subscription details
@router.get("/subscriptions/{user_id}")
def get_subscription(user_id: int, db: Session = Depends(get_db)):
    subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="No subscription found")
    return subscription

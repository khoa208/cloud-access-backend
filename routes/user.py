from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from database import SessionLocal
from schemas import UserCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new user
@router.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(name=user.name, email=user.email, password_hash="dummy_hash")  # Add hashed password logic later
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get all users
@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

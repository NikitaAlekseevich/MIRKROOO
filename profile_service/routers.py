from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Profile

profile_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@profile_router.post("/")
def create_profile(name: str, db: Session = Depends(get_db)):
    new_profile = Profile(name=name)
    db.add(new_profile)
    db.commit()
    return {"message": "Profile created"}

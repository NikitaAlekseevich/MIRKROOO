from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Profile
from uuid import uuid4
from pydantic import BaseModel

profile_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ProfileCreateRequest(BaseModel):
    name: str

# 1. Создание профиля
@profile_router.post("/")
def create_profile(request: ProfileCreateRequest, db: Session = Depends(get_db)):
    new_profile = Profile(id=str(uuid4()), name=request.name)
    db.add(new_profile)
    db.commit()
    return {"message": "Profile created"}

# 2. Получение профиля
@profile_router.get("/{profile_id}")
def get_profile(profile_id: str, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

# 3. Обновление имени профиля
@profile_router.put("/update-name/{profile_id}")
def update_name(profile_id: str, name: str, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    profile.name = name
    db.commit()
    return {"message": "Profile name updated"}

# 4. Загрузка фотографии профиля
@profile_router.post("/upload-photo/{profile_id}")
def upload_photo(profile_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    profile.photo_url = f"/static/{file.filename}"  
    db.commit()
    return {"message": "Photo uploaded"}

# 5. Обновление настроек конфиденциальности
@profile_router.put("/update-privacy/{profile_id}")
def update_privacy(profile_id: str, visibility: str, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    profile.privacy_settings = visibility
    db.commit()
    return {"message": "Privacy settings updated"}

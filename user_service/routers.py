from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from uuid import uuid4
import random

user_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Регистрация пользователя
@user_router.post("/register")
def register(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(id=str(uuid4()), email=email, password=password)
    db.add(new_user)
    db.commit()
    return {"message": "User registered"}

# 2. Вход пользователя
@user_router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email, User.password == password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

# 3. Получение профиля пользователя
@user_router.get("/profile/{user_id}")
def get_profile(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 4. Обновление пароля
@user_router.put("/update-password/{user_id}")
def update_password(user_id: str, new_password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.password = new_password
    db.commit()
    return {"message": "Password updated"}

# 5. Удаление пользователя
@user_router.delete("/delete/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

# 6. Регистрация с отправкой кода подтверждения (вложенные функции)
@user_router.post("/register-with-verification")
def register_with_verification(email: str, password: str, db: Session = Depends(get_db)):
    # Вложенная функция для создания пользователя
    def create_user(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if user:
            raise HTTPException(status_code=400, detail="Email already registered")
        new_user = User(id=str(uuid4()), email=email, password=password)
        db.add(new_user)
        db.commit()
        return new_user

    # Вложенная функция для генерации кода подтверждения
    def generate_verification_code():
        return str(random.randint(100000, 999999))  # Генерация 6-значного кода

    # Вложенная функция для отправки кода на email
    def send_verification_email(email: str, code: str):
        # Симуляция отправки email
        print(f"Verification code sent to {email}: {code}")

    # Использование вложенных функций
    user = create_user(db, email, password)  # Создаём пользователя
    verification_code = generate_verification_code()  # Генерируем код подтверждения
    send_verification_email(email, verification_code)  # Отправляем код

    return {"message": "User registered. Verification code sent to email.", "user_id": user.id}

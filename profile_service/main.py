from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, engine
from routers import profile_router

app = FastAPI(title="Profile Service")

# Проверка и создание таблиц
try:
    Base.metadata.create_all(bind=engine)
    print("✅Таблицы успешно созданы!")
except Exception as e:
    print(f"❌Ошибка создания таблиц: {e}")

app.include_router(profile_router, prefix="/profiles")

# Ручка для проверки статуса
@app.get("/health")
def health_check():
    return {"status": "Profile Service is running"}

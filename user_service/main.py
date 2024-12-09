from fastapi import FastAPI
from database import Base, engine
from routers import user_router

# Создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service")

# Включение роутеров
app.include_router(user_router, prefix="/users")

# Ручка для проверки статуса
@app.get("/health")
def health_check():
    return {"status": "User Service is running"}

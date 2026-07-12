from fastapi import FastAPI
from app.api.v1 import bookings
from app.core.database import engine, Base
from app.core.config import settings

# Создаём таблицы БД (в продакшене используйте Alembic миграции)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(bookings.router)

@app.get("/")
def root():
    return {"message": "Сервис бронирования работает!"}

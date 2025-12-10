from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone
import uuid
import os
from dotenv import load_dotenv
import logging
from contextlib import asynccontextmanager

# Завантажуємо змінні середовища
load_dotenv()

# --- Конфігурація ---
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    f"mysql+pymysql://root:sbEzVDPBjRjKOFhGhRxGnOkodutRJzLx@mysql-wlsg.railway.internal:3306/railway"
)

# Створюємо SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False  # Поставте True для дебагу SQL запитів
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Моделі бази даних ---
class StatusCheckDB(Base):
    __tablename__ = "status_checks"
    
    id = Column(String(36), primary_key=True, index=True)
    client_name = Column(String(255), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    additional_info = Column(Text, nullable=True)

# Створюємо таблиці (якщо немає)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Створюємо таблиці при запуску
    Base.metadata.create_all(bind=engine)
    print("✅ База даних готова")
    yield
    print("✅ Додаток зупинено")

# --- Pydantic моделі ---
class StatusCheckBase(BaseModel):
    client_name: str
    additional_info: Optional[str] = None

class StatusCheckCreate(StatusCheckBase):
    pass

class StatusCheckResponse(StatusCheckBase):
    id: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

# --- Залежності ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Створюємо додаток ---
app = FastAPI(
    title="My Backend API",
    description="API для зв'язку з MySQL на Railway",
    version="1.0.0",
    lifespan=lifespan
)

# --- CORS налаштування ---
# Додайте ваші домени InfinityFree сюди
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '').split(',')
if not ALLOWED_ORIGINS or ALLOWED_ORIGINS == ['']:
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        # Додайте ваші InfinityFree домени:
        # "https://ваш-сайт.infinityfreeapp.com",
        # "http://ваш-сайт.infinityfreeapp.com",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Роутер ---
api_router = APIRouter(prefix="/api")

# --- Роути ---
@api_router.get("/")
async def api_root():
    return {
        "message": "Backend API працює!",
        "database": "MySQL на Railway",
        "endpoints": {
            "GET /api/": "Це повідомлення",
            "GET /api/health": "Перевірка здоров'я",
            "POST /api/status": "Створити статус",
            "GET /api/status": "Отримати всі статуси",
            "GET /api/status/{id}": "Отримати статус по ID",
            "DELETE /api/status/{id}": "Видалити статус"
        },
        "docs": "/docs - документація Swagger",
        "frontend_guide": "Додайте ваші InfinityFree домени до ALLOWED_ORIGINS"
    }

@api_router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Перевіряємо підключення до БД
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": db_status,
        "service": "FastAPI Backend"
    }

@api_router.post("/status", response_model=StatusCheckResponse)
async def create_status(
    status: StatusCheckCreate,
    db: Session = Depends(get_db)
):
    try:
        # Генеруємо унікальний ID
        status_id = str(uuid.uuid4())
        
        # Створюємо запис у БД
        db_status = StatusCheckDB(
            id=status_id,
            client_name=status.client_name,
            additional_info=status.additional_info,
            timestamp=datetime.now(timezone.utc)
        )
        
        db.add(db_status)
        db.commit()
        db.refresh(db_status)
        
        return db_status
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Помилка створення: {str(e)}")

@api_router.get("/status", response_model=List[StatusCheckResponse])
async def get_all_statuses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    try:
        statuses = db.query(StatusCheckDB)\
            .order_by(StatusCheckDB.timestamp.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
        return statuses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка отримання: {str(e)}")

@api_router.get("/status/{status_id}", response_model=StatusCheckResponse)
async def get_status(
    status_id: str,
    db: Session = Depends(get_db)
):
    status = db.query(StatusCheckDB).filter(StatusCheckDB.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Статус не знайдено")
    return status

@api_router.delete("/status/{status_id}")
async def delete_status(
    status_id: str,
    db: Session = Depends(get_db)
):
    try:
        status = db.query(StatusCheckDB).filter(StatusCheckDB.id == status_id).first()
        if not status:
            raise HTTPException(status_code=404, detail="Статус не знайдено")
        
        db.delete(status)
        db.commit()
        
        return {"message": "Статус успішно видалено", "id": status_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Помилка видалення: {str(e)}")

# Додаємо роутер до додатку
app.include_router(api_router)

# --- Кореневий роут ---
@app.get("/")
async def root():
    return {
        "message": "Головна сторінка Backend API",
        "service": "FastAPI + MySQL на Railway",
        "frontend": "Підключіть ваш InfinityFree сайт",
        "endpoints": {
            "api_docs": "/docs",
            "api_root": "/api",
            "health_check": "/api/health"
        }
    }

# --- Налаштування логування ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Обробка помилок ---
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Глобальна помилка: {exc}")
    return {
        "error": "Внутрішня помилка сервера",
        "details": str(exc) if os.getenv("DEBUG") == "True" else None
    }

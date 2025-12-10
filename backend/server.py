from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, DateTime, Text, inspect
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

# --- Конфігурація MySQL ---
# Беремо дані з Railway (які ви надали)
MYSQL_HOST = "mysql-wlsg.railway.internal"
MYSQL_USER = "root"
MYSQL_PASSWORD = "sbEzVDPBjRjKOFhGhRxGnOkodutRJzLx"
MYSQL_PORT = 3306
MYSQL_DATABASE = "railway"

# Формуємо URL для SQLAlchemy
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Створюємо SQLAlchemy engine з оптимізацією
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Перевіряє з'єднання перед використанням
    pool_recycle=3600,   # Оновлює з'єднання кожну годину
    pool_size=5,         # Мінімальна кількість з'єднань
    max_overflow=10,     # Максимальна кількість з'єднань
    echo=False          # Поставте True для дебагу SQL
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
    ip_address = Column(String(45), nullable=True)  # IPv6 може бути 45 символів
    user_agent = Column(Text, nullable=True)

# --- Lifespan для управління життєвим циклом ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управління життєвим циклом додатку.
    Створює таблиці при старті, закриває з'єднання при завершенні.
    """
    print("🚀 Запуск FastAPI додатку...")
    
    try:
        # Перевіряємо підключення до MySQL
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("✅ Підключено до MySQL на Railway")
        
        # Створюємо таблиці (якщо не існують)
        Base.metadata.create_all(bind=engine)
        print("✅ Таблиці бази даних готові")
        
    except Exception as e:
        print(f"❌ Помилка підключення до MySQL: {e}")
        raise
    
    yield
    
    # Завершення роботи
    print("🔌 Закриття з'єднань з базою даних...")
    engine.dispose()
    print("✅ Додаток зупинено")

# --- Pydantic моделі для валідації ---
class StatusCheckCreate(BaseModel):
    client_name: str
    additional_info: Optional[str] = None

class StatusCheckResponse(BaseModel):
    id: str
    client_name: str
    timestamp: datetime
    additional_info: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    
    class Config:
        from_attributes = True  # Для роботи з SQLAlchemy об'єктами

# --- Залежність для отримання сесії БД ---
def get_db():
    """
    Залежність для отримання сесії бази даних.
    Автоматично закриває сесію після використання.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Створення FastAPI додатку ---
app = FastAPI(
    title="My Backend API",
    description="API для зв'язку з MySQL на Railway",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# --- CORS налаштування для InfinityFree ---
# Додайте ваш реальний домен InfinityFree сюди
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '').split(',')
if not ALLOWED_ORIGINS or ALLOWED_ORIGINS == ['']:
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "https://localhost:3000",
        # Додайте ваші реальні домени:
        # "https://your-site.infinityfreeapp.com",
        # "http://your-site.infinityfreeapp.com",
        # "*"  # Тимчасово для тестування (не для продакшн!)
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600  # Кешування preflight запитів на 10 хвилин
)

# --- Роутер з префіксом /api ---
api_router = APIRouter(prefix="/api", tags=["API"])

# --- Роути API ---
@api_router.get("/", summary="Головна сторінка API")
async def api_root():
    """Повертає інформацію про доступні ендпоінти API."""
    return {
        "message": "🚀 Backend API успішно працює!",
        "database": "MySQL на Railway",
        "status": "active",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "endpoints": {
            "GET /api/": "Це повідомлення",
            "GET /api/health": "Перевірка здоров'я системи",
            "POST /api/status": "Створити новий статус",
            "GET /api/status": "Отримати всі статуси",
            "GET /api/status/{id}": "Отримати статус по ID",
            "DELETE /api/status/{id}": "Видалити статус"
        },
        "docs": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }

@api_router.get("/health", summary="Перевірка здоров'я системи")
async def health_check(db: Session = Depends(get_db)):
    """
    Перевіряє стан системи та підключення до бази даних.
    """
    try:
        # Перевіряємо підключення до БД
        db.execute("SELECT 1")
        
        # Рахуємо кількість записів
        count = db.query(StatusCheckDB).count()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "database": {
                "status": "connected",
                "type": "MySQL",
                "host": MYSQL_HOST,
                "records_count": count
            },
            "service": "FastAPI Backend",
            "version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Помилка бази даних: {str(e)}"
        )

@api_router.post("/status", 
                response_model=StatusCheckResponse,
                status_code=status.HTTP_201_CREATED,
                summary="Створити новий статус")
async def create_status(
    status_data: StatusCheckCreate,
    db: Session = Depends(get_db)
):
    """
    Створює новий запис статусу в базі даних.
    """
    try:
        # Генеруємо унікальний ID
        status_id = str(uuid.uuid4())
        
        # Створюємо запис у БД
        db_status = StatusCheckDB(
            id=status_id,
            client_name=status_data.client_name,
            additional_info=status_data.additional_info,
            timestamp=datetime.now(timezone.utc)
        )
        
        db.add(db_status)
        db.commit()
        db.refresh(db_status)
        
        return db_status
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Помилка створення запису: {str(e)}"
        )

@api_router.get("/status", 
                response_model=List[StatusCheckResponse],
                summary="Отримати всі статуси")
async def get_all_statuses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Повертає список всіх статусів з пагінацією.
    """
    try:
        statuses = db.query(StatusCheckDB)\
            .order_by(StatusCheckDB.timestamp.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
        return statuses
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Помилка отримання даних: {str(e)}"
        )

@api_router.get("/status/{status_id}", 
                response_model=StatusCheckResponse,
                summary="Отримати статус по ID")
async def get_status(
    status_id: str,
    db: Session = Depends(get_db)
):
    """
    Повертає конкретний статус за його ID.
    """
    status = db.query(StatusCheckDB).filter(StatusCheckDB.id == status_id).first()
    if not status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Статус з таким ID не знайдено"
        )
    return status

@api_router.delete("/status/{status_id}", 
                   summary="Видалити статус")
async def delete_status(
    status_id: str,
    db: Session = Depends(get_db)
):
    """
    Видаляє статус за його ID.
    """
    try:
        status = db.query(StatusCheckDB).filter(StatusCheckDB.id == status_id).first()
        if not status:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Статус з таким ID не знайдено"
            )
        
        db.delete(status)
        db.commit()
        
        return {
            "message": "Статус успішно видалено",
            "id": status_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Помилка видалення: {str(e)}"
        )

# Додаємо роутер до додатку
app.include_router(api_router)

# --- Додаткові глобальні роути ---
@app.get("/", include_in_schema=False)
async def root():
    """Перенаправляє на API документацію."""
    return {
        "message": "Ласкаво просимо до Backend API!",
        "service": "FastAPI + MySQL на Railway",
        "frontend": "Підключіть ваш InfinityFree сайт",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "api_root": "/api"
        },
        "health_check": "/api/health",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/ping", include_in_schema=False)
async def ping():
    """Простий ендпоінт для пінгування сервера."""
    return {"ping": "pong", "timestamp": datetime.now(timezone.utc).isoformat()}

# --- Налаштування логування ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# --- Глобальний обробник помилок ---
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.warning(f"HTTP помилка: {exc.status_code} - {exc.detail}")
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Неочікувана помилка: {exc}", exc_info=True)
    return {
        "error": "Внутрішня помилка сервера",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# --- Запуск додатку (для локального тестування) ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

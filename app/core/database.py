from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sqlalchemy_database_url = "sqlite:///./bookings.db"

engine = create_engine(sqlalchemy_database_url, connect_args={"check_same_thread": False})#Создание движка для подключения к бд
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)#Создание сессий
Base = declarative_base()#Базовый класс для моделей

def get_db():#Получение сессии
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

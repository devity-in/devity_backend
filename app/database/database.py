from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from sqlalchemy import inspect




DATABASE_URL = settings.DATABASE_URL
# print("Database URL: ", DATABASE_URL)
# connect_args={"check_same_thread": False} is specific of sqlite
# Using the URL from .env is unable to detect database type so putting here directly
# engine = create_engine(
#     "postgresql://casaos:casaos@192.168.0.109:5432/casaos",
# )

engine = create_engine(
    DATABASE_URL,
    echo=False,
)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


        
def init_db():
    from app.database import models
    
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    # Reflect existing tables
    Base.metadata.reflect(engine)
    
    # Create only the tables that don't exist
    Base.metadata.create_all(bind=engine, checkfirst=True)
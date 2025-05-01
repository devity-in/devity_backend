from sqlmodel import SQLModel, create_engine, Session, inspect
from sqlalchemy.orm import sessionmaker
from app.config import settings

DATABASE_URL = settings.DATABASE_URL
# print("Database URL: ", DATABASE_URL)
# connect_args={"check_same_thread": False} is specific of sqlite
# Using the URL from .env is unable to detect database type so putting here directly
# engine = create_engine(
#     "postgresql://casaos:casaos@192.168.0.109:5432/casaos",
# )

engine = create_engine(
    str(DATABASE_URL),
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

def create_db_and_tables():
    # Import models here to ensure they are registered with SQLModel.metadata
    # IMPORTANT: Add imports for ALL your SQLModel models here
    from app.database.models.spec import Spec 
    # from app.database.models.project import Project # Removed import as Project model/dependency is not used in M1

    print("Creating database tables...")
    try:
        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        # Consider more robust error handling or re-raising

# Rename init_db to avoid confusion, we call create_db_and_tables explicitly
# def init_db():
#     ...
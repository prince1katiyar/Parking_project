

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "sqlite:///./data/parking.db"


os.makedirs("./data", exist_ok=True)

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_and_tables():
    print("DATABASE: Attempting to create tables...")
    try:
      
        from . import models 
        Base.metadata.create_all(bind=engine)
        print("DATABASE: Base.metadata.create_all(bind=engine) executed.")
    except Exception as e:
        print(f"DATABASE: ERROR during table creation: {e}")
        raise 
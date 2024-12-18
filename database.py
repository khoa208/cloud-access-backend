from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL "postgresql://username:password@localhost:5432/name of the database"
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/CloudAccess"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

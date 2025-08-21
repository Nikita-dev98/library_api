from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# PostgreSQL connection string
database_url = "postgresql+psycopg2://library_user:qwerty@localhost:5432/library"

engine = create_engine(database_url)
localSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

# db session for each request
def get_db():
    db = localSession()
    try:
        yield db
    finally:
        db.close()
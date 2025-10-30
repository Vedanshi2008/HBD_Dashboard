from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# Base class for all models
Base = declarative_base()

# Database URL (MySQL)
# DATABASE_URL = "mysql+pymysql://genuineh_dashboard:Wecandoit_2025@mumult1.hostarmada.net:3306/genuineh_dashboard"
DATABASE_URL = "mysql+pymysql://root:vivek123@localhost:3306/dummy"
# DATABASE_URL = "mysql+pymysql://genuineh_dashboard:Wecandoit_2025@localhost:3306/genuineh_dashboard"

# Engine creation
engine = create_engine(
    DATABASE_URL,
    echo=True,              
    future=True,
    pool_pre_ping=True,    
    pool_recycle=3600       
)

# Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Scoped session (thread-safe)
db_session = scoped_session(SessionLocal)

# Utility function to get a session
def get_db_session():
    """
    Returns a new database session.
    In Flask routes you must close() manually after use.
    """
    return db_session()

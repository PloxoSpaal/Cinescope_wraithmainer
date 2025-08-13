from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Integer, text, Enum
from sqlalchemy.orm import declarative_base, sessionmaker, Session


Base = declarative_base()


class UserTableDBSchema(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    email = Column(String)
    full_name = Column(String)
    password = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    verified = Column(Boolean)
    banned = Column(Boolean)
    roles = Column(Enum)
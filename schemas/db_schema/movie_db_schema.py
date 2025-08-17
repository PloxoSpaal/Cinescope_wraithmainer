from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Integer, text, Float, Enum
from sqlalchemy.orm import declarative_base, sessionmaker, Session


Base = declarative_base()


class MovieTableDBSchema(Base):
    __tablename__ = 'movies'
    id = Column(String, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    description = Column(String)
    image_url = Column(String)
    location = Column(String)
    published = Column(Boolean)
    rating = Column(Float)
    genre_id = Column(String)
    created_at = Column(DateTime)
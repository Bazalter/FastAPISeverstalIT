from sqlalchemy import Column, Float, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Roll(Base):
    __tablename__ = 'rolls'

    id = Column(Integer, primary_key=True, index=True)
    length = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow)
    date_removed = Column(DateTime, nullable=False)

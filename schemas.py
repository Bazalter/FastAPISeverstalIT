from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RollCreate(BaseModel):
    length: float
    weight: float


class Roll(BaseModel):
    id: int
    length: float
    weight: float
    date_added: datetime
    date_removed: Optional[datetime]

    class Config:
        from_attributes = True


class RollDateDelete(BaseModel):
    date_removed: datetime
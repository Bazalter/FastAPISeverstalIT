from sqlalchemy import Float, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from database import Base


class Roll(Base):
    __tablename__ = 'rolls'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    length: Mapped[float] = mapped_column(Float, nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    date_added: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    date_removed: Mapped[datetime] = mapped_column(DateTime, nullable=True)

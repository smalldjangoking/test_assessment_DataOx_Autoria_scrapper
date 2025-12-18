from .database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, BigInteger
from datetime import datetime, timezone

class Autoria_model(Base):
    __tablename__ = "auto_ria"
    

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String)
    price_usd: Mapped[int] = mapped_column(Integer)
    odometer: Mapped[int] = mapped_column(Integer)
    username: Mapped[str] = mapped_column(String)
    phone_number: Mapped[int] = mapped_column(BigInteger)
    image_url: Mapped[str] = mapped_column(String)
    images_count: Mapped[int] = mapped_column(Integer)
    car_number: Mapped[str] = mapped_column(String, nullable=True)
    car_vin: Mapped[str] = mapped_column(String, nullable=True)
    datetime_found: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))







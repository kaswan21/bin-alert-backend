from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

class Bin(Base):
    __tablename__ = "bins"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    location: Mapped[str | None] = mapped_column(String(255), nullable=False)
    warning_threshold: Mapped[int] = mapped_column(Integer, nullable=False,default=80)
    full_threshold: Mapped[int] = mapped_column(Integer, nullable=False,default=95)
    current_level: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    readings = relationship("Reading", back_populates="bin", cascade="all,delete-orphan")
    alerts = relationship("Alert", back_populates="bin", cascade="all,delete-orphan")

    __table_args__=(
        CheckConstraint("warning_threshold >= 0 AND warning_threshold <= 100", name="ck_bins_warning_0_100"),
        CheckConstraint("full_threshold >= 0 AND full_threshold <= 100", name="ck_bins_full_0_100"),
        CheckConstraint("full_threshold >= warning_threshold", name="ck_bins_full_gte_warning"),
        CheckConstraint("current_level >= 0 AND current_level <= 100", name="ck_bins_current_level_0_100"),
   
       )


class Reading(Base):
    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    bin_id: Mapped[int] = mapped_column(ForeignKey("bins.id", ondelete="CASCADE"), nullable=False, index=True)

    fill_percent: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    bin = relationship("Bin", back_populates="readings")

    __table_args__ = (
        CheckConstraint("fill_percent >= 0 AND fill_percent <= 100", name="ck_readings_fill_0_100"),
    )

class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    bin_id: Mapped[int] = mapped_column(ForeignKey("bins.id", ondelete="CASCADE"), nullable=False, index=True)

    level: Mapped[str] = mapped_column(String(16), nullable=False)  # WARNING | FULL
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="OPEN")  # OPEN|ACK|RESOLVED

    message: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    bin = relationship("Bin", back_populates="alerts")
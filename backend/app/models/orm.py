"""مدل‌های ORM مطابق طرح جدول‌های سند TCOP (مطابق بخش ۶.۱ SRS)"""
from __future__ import annotations

from datetime import datetime, date
from sqlalchemy import (
    String, Integer, Float, Boolean, DateTime, Date, JSON, ForeignKey, Text, BigInteger
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Press(Base):
    __tablename__ = "presses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    model: Mapped[str | None] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(16), default="active")
    installed_at: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Compound(Base):
    __tablename__ = "compounds"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    name: Mapped[str | None] = mapped_column(String(128))
    spec_json: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Tire(Base):
    __tablename__ = "tires"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    compound_id: Mapped[int | None] = mapped_column(ForeignKey("compounds.id"))
    structure_json: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Mold(Base):
    __tablename__ = "molds"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    press_id: Mapped[int | None] = mapped_column(ForeignKey("presses.id"))
    status: Mapped[str] = mapped_column(String(16), default="ok")
    total_cycles: Mapped[int] = mapped_column(Integer, default=0)
    last_service: Mapped[date | None] = mapped_column(Date)


class CureCycle(Base):
    """در SQLite از Integer استفاده می‌کنیم تا قاعده INTEGER PRIMARY KEY
    (افزایش خودکار) به‌درستی اعمال شود."""
    __tablename__ = "cure_cycles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    press_id: Mapped[int | None] = mapped_column(ForeignKey("presses.id"))
    tire_id: Mapped[int | None] = mapped_column(ForeignKey("tires.id"))
    mold_id: Mapped[int | None] = mapped_column(ForeignKey("molds.id"))
    start_ts: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_ts: Mapped[datetime | None]
    duration_min: Mapped[float | None] = mapped_column(Float)
    steam_pressure: Mapped[float | None] = mapped_column(Float)
    hot_water_temp: Mapped[float | None] = mapped_column(Float)
    nitrogen_pressure: Mapped[float | None] = mapped_column(Float)
    energy_kwh: Mapped[float | None] = mapped_column(Float)
    source: Mapped[str] = mapped_column(String(16), default="synthetic")


class SensorReading(Base):
    __tablename__ = "sensor_readings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    press_id: Mapped[int | None]
    sensor: Mapped[str] = mapped_column(String(32))
    value: Mapped[float] = mapped_column(Float)


class QualityTest(Base):
    __tablename__ = "quality_tests"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tire_id: Mapped[int | None] = mapped_column(ForeignKey("tires.id"))
    test_type: Mapped[str | None] = mapped_column(String(32))
    result_json: Mapped[dict | None] = mapped_column(JSON)
    passed: Mapped[bool | None] = mapped_column(Boolean)
    tested_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Prediction(Base):
    __tablename__ = "predictions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cure_cycle_id: Mapped[int | None] = mapped_column(Integer)
    cure_degree: Mapped[float | None] = mapped_column(Float)
    quality_prob: Mapped[float | None] = mapped_column(Float)
    anomaly_score: Mapped[float | None] = mapped_column(Float)
    model_version: Mapped[str | None] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(String(32), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

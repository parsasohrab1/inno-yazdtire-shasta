"""نشست پایگاه داده و ابزار ساخت جداول"""
from __future__ import annotations

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import DATABASE_URL
from app.models.orm import Base

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    future=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    """ایجاد تمام جداول تعریف‌شده (۹ جدول مطابق SRS)"""
    Base.metadata.create_all(bind=engine)


@contextmanager
def session_scope() -> Session:
    """مدیریت نشست تراکنشی"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db():
    """وابستگی FastAPI برای تزریق نشست"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""تنظیمات مشترک pytest: مسیر ایمپورت و پایگاه داده آزمایشی"""
import os
import sys
import tempfile
from pathlib import Path

# افزودن مسیر پروژه
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))
sys.path.insert(0, str(ROOT / "scripts"))

# استفاده از پایگاه داده موقت برای تست‌ها
TEST_DB = tempfile.mktemp(suffix=".db")
os.environ["TCOP_DATABASE_URL"] = f"sqlite:///{TEST_DB}"

import pytest
from app.db.session import engine, init_db, SessionLocal
from app.models.orm import Base


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """راه‌اندازی پایگاه داده آزمایشی برای کل نشست"""
    init_db()
    yield
    # پاکسازی
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    """نشست پایگاه داده برای هر تست"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        # پاک‌سازی داده‌های تست
        with engine.begin() as conn:
            for tbl in ["predictions", "quality_tests", "sensor_readings",
                        "cure_cycles", "molds", "tires", "compounds",
                        "presses", "users"]:
                conn.exec_driver_sql(f"DELETE FROM {tbl}")

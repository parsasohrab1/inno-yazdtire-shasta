"""تست‌های واحد مدل‌های ORM و پایگاه داده"""
import pytest
from datetime import datetime, date

from app.models.orm import (
    Press, Compound, Tire, Mold, CureCycle, SensorReading,
    QualityTest, Prediction, User,
)
from app.db.session import session_scope, init_db


class TestORMModels:

    def test_create_press(self, db_session):
        p = Press(name="Press-Test", model="TEST-001", status="active",
                  installed_at=date(2024, 1, 1))
        db_session.add(p)
        db_session.flush()
        assert p.id is not None
        assert p.name == "Press-Test"
        assert p.status == "active"

    def test_create_compound(self, db_session):
        c = Compound(code="CMP-TEST", name="Test Compound",
                     spec_json={"density": 1.15, "k": 0.25})
        db_session.add(c)
        db_session.flush()
        assert c.id is not None
        assert c.spec_json["density"] == 1.15

    def test_create_tire_with_compound(self, db_session):
        c = Compound(code="CMP-T1", name="T1")
        db_session.add(c)
        db_session.flush()
        t = Tire(code="TIRE-T1", compound_id=c.id,
                 structure_json={"width": 205, "ratio": 55})
        db_session.add(t)
        db_session.flush()
        assert t.id is not None
        assert t.compound_id == c.id

    def test_create_mold(self, db_session):
        p = Press(name="Press-M1")
        db_session.add(p)
        db_session.flush()
        m = Mold(code="MOLD-T1", press_id=p.id, status="ok",
                 total_cycles=100)
        db_session.add(m)
        db_session.flush()
        assert m.id is not None
        assert m.press_id == p.id
        assert m.total_cycles == 100

    def test_create_cure_cycle(self, db_session):
        cc = CureCycle(
            press_id=None, tire_id=None, mold_id=None,
            start_ts=datetime(2025, 1, 1, 10, 0, 0),
            end_ts=datetime(2025, 1, 1, 10, 25, 0),
            duration_min=25.0, steam_pressure=1.5,
            hot_water_temp=170.0, nitrogen_pressure=1.2,
            energy_kwh=55.0, source="synthetic",
        )
        db_session.add(cc)
        db_session.flush()
        assert cc.id is not None
        assert cc.duration_min == 25.0
        assert cc.source == "synthetic"

    def test_create_sensor_reading(self, db_session):
        sr = SensorReading(
            time=datetime(2025, 1, 1, 10, 0, 0),
            press_id=1, sensor="temp", value=170.5,
        )
        db_session.add(sr)
        db_session.flush()
        assert sr.id is not None
        assert sr.value == 170.5

    def test_create_quality_test(self, db_session):
        qt = QualityTest(
            tire_id=None, test_type="uniformity",
            result_json={"radial": 1.5, "lateral": 2.0},
            passed=True,
        )
        db_session.add(qt)
        db_session.flush()
        assert qt.id is not None
        assert qt.passed is True

    def test_create_prediction(self, db_session):
        p = Prediction(
            cure_cycle_id=1, cure_degree=0.95,
            quality_prob=0.92, anomaly_score=0.1,
            model_version="test-v1.0",
        )
        db_session.add(p)
        db_session.flush()
        assert p.id is not None
        assert p.cure_degree == 0.95

    def test_create_user(self, db_session):
        u = User(username="test_user", password_hash="hash123",
                 role="admin", is_active=True)
        db_session.add(u)
        db_session.flush()
        assert u.id is not None
        assert u.role == "admin"
        assert u.is_active is True

    def test_init_db_creates_all_tables(self):
        # init_db باید تمام ۹ جدول را ایجاد کند
        init_db()
        from sqlalchemy import inspect
        insp = inspect(__import__("app.db.session", fromlist=["engine"]).engine)
        tables = insp.get_table_names()
        expected = ["presses", "compounds", "tires", "molds",
                    "cure_cycles", "sensor_readings", "quality_tests",
                    "predictions", "users"]
        for tbl in expected:
            assert tbl in tables, f"جدول {tbl} ایجاد نشده است"

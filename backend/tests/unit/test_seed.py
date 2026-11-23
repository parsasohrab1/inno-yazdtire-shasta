"""تست‌های واحد بارگذاری داده‌های مصنوعی"""
import pytest

from app.db.seed import (
    generate_presses, generate_compounds, generate_tires,
    generate_molds, generate_cycles_and_predictions,
    generate_quality_tests, load_synthetic_data, _d,
)
from app.db.session import session_scope
from app.models.orm import Press, Compound, Tire, Mold, CureCycle, Prediction


class TestDataGenerators:

    def test_generate_presses(self):
        presses = generate_presses()
        assert len(presses) == 15
        assert all("name" in p for p in presses)
        assert all("model" in p for p in presses)

    def test_generate_compounds(self):
        compounds = generate_compounds()
        assert len(compounds) == 3
        codes = [c["code"] for c in compounds]
        assert "CMP-A1" in codes
        assert "CMP-B2" in codes
        assert "CMP-C3" in codes

    def test_generate_tires(self):
        tires = generate_tires()
        assert len(tires) == 100
        # هر تایر باید ساختار داشته باشد
        assert "structure_json" in tires[0]
        assert "width" in tires[0]["structure_json"]

    def test_generate_molds(self):
        molds = generate_molds()
        assert len(molds) == 30
        assert all("total_cycles" in m for m in molds)

    def test_generate_cycles_and_predictions(self):
        cycles, sensors, preds = generate_cycles_and_predictions()
        assert len(cycles) == 2000
        assert len(sensors) == 20000  # ۱۰ سنسور برای هر چرخه
        assert len(preds) == 2000
        # بررسی تنوع برچسب‌های کیفیت
        qualities = [p["quality_prob"] for p in preds]
        assert min(qualities) < 0.7
        assert max(qualities) > 0.9

    def test_generate_quality_tests(self):
        qts = generate_quality_tests()
        # ۳ آزمون برای ۱۰۰ تایر
        assert len(qts) == 300
        assert all("passed" in q for q in qts)
        assert all("result_json" in q for q in qts)

    def test_date_helper(self):
        d = _d("2024-01-15")
        assert d.year == 2024 and d.month == 1 and d.day == 15
        # None ورودی → None خروجی
        assert _d(None) is None
        assert _d("") is None


class TestLoadSyntheticData:

    def test_load_returns_counts(self):
        counts = load_synthetic_data(verbose=False)
        assert "presses" in counts
        assert "compounds" in counts
        assert "tires" in counts
        assert "cure_cycles" in counts
        assert counts["presses"] == 15
        assert counts["compounds"] == 3
        assert counts["cure_cycles"] == 2000

    def test_data_persisted_in_db(self):
        with session_scope() as s:
            assert s.query(Press).count() == 15
            assert s.query(Compound).count() == 3
            assert s.query(Tire).count() == 100
            assert s.query(Mold).count() == 30
            assert s.query(CureCycle).count() == 2000
            assert s.query(Prediction).count() == 2000

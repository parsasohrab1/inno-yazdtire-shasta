"""تست‌های واحد بارگذاری داده‌های واقعی"""
import os
import pytest
import numpy as np
from pathlib import Path

from app.core.config import AI4I_CSV, SECOM_DATA, SECOM_LABELS
from app.db.load_real import load_ai4i_rows, load_secom_features, _d
from app.db.session import session_scope
from app.models.orm import (
    Press, Compound, Tire, Mold, CureCycle, QualityTest, Prediction,
)


def _has_real_files():
    """بررسی وجود فایل‌های داده واقعی"""
    return AI4I_CSV.exists() and SECOM_DATA.exists() and SECOM_LABELS.exists()


pytestmark = pytest.mark.skipif(
    not _has_real_files(),
    reason="فایل‌های داده واقعی (AI4I/SECOM) موجود نیستند",
)


class TestDateHelper:

    def test_d_parses_iso(self):
        d = _d("2024-06-15")
        assert d.year == 2024 and d.month == 6 and d.day == 15

    def test_d_handles_none(self):
        assert _d(None) is None
        assert _d("") is None

    def test_d_handles_invalid(self):
        assert _d("not-a-date") is None

    def test_d_passthrough_date(self):
        import datetime
        d0 = datetime.date(2024, 1, 1)
        assert _d(d0) == d0


class TestLoadAI4I:

    def test_load_returns_counts(self, db_session):
        """بارگذاری داده واقعی AI4I باید تمام جداول را پر کند"""
        counts = load_ai4i_rows(verbose=False)
        if "skipped" in counts and counts["skipped"]:
            # اگر قبلاً بارگذاری شده، شمارش‌ها از DB خوانده می‌شوند
            pass
        assert "presses" in counts or "skipped" in counts
        if "presses" in counts:
            assert counts["presses"] == 3
            assert counts["cure_cycles"] == 1000

    def test_real_data_in_db(self, db_session):
        """بررسی ذخیره‌سازی داده واقعی در DB"""
        load_ai4i_rows(verbose=False)
        with session_scope() as s:
            real_presses = s.query(Press).filter(
                Press.name.like("Press-Real-%")).count()
            assert real_presses == 3
            real_cycles = s.query(CureCycle).filter(
                CureCycle.source == "real").count()
            assert real_cycles == 1000

    def test_real_predictions_persisted(self, db_session):
        load_ai4i_rows(verbose=False)
        with session_scope() as s:
            real_preds = s.query(Prediction).filter(
                Prediction.model_version == "real-v1.0").count()
            assert real_preds == 1000

    def test_real_quality_tests_persisted(self, db_session):
        load_ai4i_rows(verbose=False)
        with session_scope() as s:
            qts = s.query(QualityTest).count()
            assert qts >= 1000

    def test_idempotent_loading(self, db_session):
        """بارگذاری مجدد نباید داده‌های تکراری ایجاد کند"""
        counts1 = load_ai4i_rows(verbose=False)
        counts2 = load_ai4i_rows(verbose=False)
        # بارگذاری دوم باید skip شود
        assert counts2 == {"skipped": True}


class TestLoadSECOM:

    def test_secom_features_loaded(self):
        info = load_secom_features(verbose=False)
        assert "X" in info
        assert "y" in info
        assert "raw_shape" in info

    def test_secom_shape(self):
        info = load_secom_features(verbose=False)
        # SECOM: 1567 نمونه، 590 ویژگی
        assert info["raw_shape"][0] == 1567
        assert info["raw_shape"][1] == 590

    def test_secom_reduced_dim(self):
        info = load_secom_features(verbose=False)
        # کاهش به ۷ مؤلفه PCA
        assert info["X"].shape[1] == 7

    def test_secom_labels_binary(self):
        info = load_secom_features(verbose=False)
        assert set(np.unique(info["y"])).issubset({0, 1})

    def test_secom_no_nan(self):
        """مقادیر گمشده باید با میانه جایگزین شده باشند"""
        info = load_secom_features(verbose=False)
        assert not np.any(np.isnan(info["X"]))

    def test_secom_pass_rate_low(self):
        """نرخ قبولی SECOM باید پایین باشد (~۷٪)"""
        info = load_secom_features(verbose=False)
        assert 0.0 < info["y"].mean() < 0.15

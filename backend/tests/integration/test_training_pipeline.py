"""تست‌های یکپارچه‌سازی: خط لوله آموزش کامل"""
import os
import json
import pytest
import numpy as np
from pathlib import Path

# فقط اگر آرتیفکت‌های آموزش ذخیره شده باشند اجرا می‌شود
ARTIFACTS = Path(__file__).resolve().parents[2] / "app" / "ml" / "artifacts"
TRAIN_REPORT = ARTIFACTS / "train_report.json"


@pytest.fixture(scope="module")
def report():
    if not TRAIN_REPORT.exists():
        pytest.skip("گزارش آموزش یافت نشد — ابتدا train_models.py را اجرا کنید")
    with open(TRAIN_REPORT) as f:
        return json.load(f)


class TestTrainingPipeline:

    def test_report_has_timestamp(self, report):
        assert "timestamp" in report

    def test_report_has_datasets(self, report):
        assert "datasets" in report
        assert "real" in report["datasets"]
        assert "synthetic" in report["datasets"]

    def test_real_data_loaded(self, report):
        real = report["datasets"]["real"]
        assert "ai4i_counts" in real
        assert real["ai4i_counts"]["cure_cycles"] == 1000
        assert real["secom_shape"][0] == 1567

    def test_synthetic_data_loaded(self, report):
        synth = report["datasets"]["synthetic"]
        assert synth["cure_cycles"] == 2000

    def test_quality_real_above_threshold(self, report):
        """دقت مدل کیفیت روی داده واقعی باید > ۹۰٪ باشد"""
        q = report["models"]["quality_real"]["test_metrics"]
        assert q["accuracy"] >= 0.90, f"دقت {q['accuracy']} زیر ۹۰٪ است"
        assert q["auc"] >= 0.90

    def test_quality_synthetic_above_threshold(self, report):
        """دقت مدل کیفیت روی داده مصنوعی باید > ۹۰٪ باشد"""
        q = report["models"]["quality_synthetic"]["test_metrics"]
        assert q["accuracy"] >= 0.90, f"دقت {q['accuracy']} زیر ۹۰٪ است"
        assert q["auc"] >= 0.90

    def test_energy_model_acceptable(self, report):
        """مدل پیش‌بینی انرژی باید قابل قبول باشد"""
        for key in ("energy_real", "energy_synthetic"):
            e = report["models"][key]
            assert e["mape"] < 0.2  # MAPE کمتر از ۲۰٪

    def test_anomaly_detector_runs(self, report):
        """آشکارساز ناهنجاری باید اجرا شده باشد"""
        for key in ("anomaly_real", "anomaly_synthetic"):
            a = report["models"][key]
            assert "anomaly_rate" in a
            assert 0 <= a["anomaly_rate"] <= 0.5

    def test_optimizer_demo(self, report):
        """بهینه‌ساز چرخه پخت باید خروجی معتبر بدهد"""
        for key in ("optimizer_demo_real", "optimizer_demo_synthetic"):
            o = report[key]
            assert "optimal_time_min" in o
            assert o["optimal_time_min"] > 0


class TestArtifactsExist:

    def test_quality_artifact_real(self):
        assert (ARTIFACTS / "quality_real.pkl").exists()

    def test_quality_artifact_synthetic(self):
        assert (ARTIFACTS / "quality_synthetic.pkl").exists()

    def test_anomaly_artifact_real(self):
        assert (ARTIFACTS / "anomaly_real.pkl").exists()

    def test_quality_artifact_secom(self):
        assert (ARTIFACTS / "quality_secom.pkl").exists()

    def test_train_report_exists(self):
        assert TRAIN_REPORT.exists()

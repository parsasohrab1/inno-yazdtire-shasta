"""تست‌های واحد مدل‌های ML: QualityPredictor، AnomalyDetector، EnergyPredictor"""
import numpy as np
import pytest

from app.services.ml_models import (
    QualityPredictor, AnomalyDetector, EnergyPredictor,
    CureOptimizer, CureCycleInput, FEATURE_COLS,
)
from app.services.heat_transfer import HeatTransferModel
from app.services.cure_kinetics import CureKineticsModel


def _make_classification_data(n=200, positive_rate=0.7, seed=42):
    rng = np.random.RandomState(seed)
    X = rng.uniform(size=(n, len(FEATURE_COLS)))
    # قانون ساده: مجموع ویژگی‌ها > آستانه → برچسب ۱
    score = X.sum(axis=1)
    threshold = np.quantile(score, 1 - positive_rate)
    y = (score >= threshold).astype(int)
    return X, y


class TestQualityPredictor:

    def test_fit_and_predict(self, tmp_path):
        X, y = _make_classification_data(200, 0.7)
        qp = QualityPredictor(model_path=str(tmp_path / "q.pkl"))
        metrics = qp.fit(X, y)
        assert "accuracy" in metrics
        assert "auc" in metrics
        # مدل باید بهتر از تصادفی باشد
        assert metrics["accuracy"] > 0.6

    def test_predict_proba_range(self, tmp_path):
        X, y = _make_classification_data(200, 0.7)
        qp = QualityPredictor(model_path=str(tmp_path / "q.pkl"))
        qp.fit(X, y)
        proba = qp.predict_proba(X)
        assert np.all(proba >= 0.0) and np.all(proba <= 1.0)

    def test_predict_single(self, tmp_path):
        X, y = _make_classification_data(100, 0.5)
        qp = QualityPredictor(model_path=str(tmp_path / "q.pkl"))
        qp.fit(X, y)
        result = qp.predict(X[0])
        assert 0 <= result.quality_prob <= 1
        assert result.predicted_label in (0, 1)

    def test_save_and_load(self, tmp_path):
        X, y = _make_classification_data(100, 0.5)
        path = str(tmp_path / "q.pkl")
        qp = QualityPredictor(model_path=path)
        qp.fit(X, y)
        # بارگذاری مجدد
        qp2 = QualityPredictor(model_path=path)
        proba1 = qp.predict_proba(X[:5])
        proba2 = qp2.predict_proba(X[:5])
        np.testing.assert_allclose(proba1, proba2, atol=1e-6)

    def test_predict_without_fit_raises(self):
        qp = QualityPredictor(model_path="/tmp/nonexistent_path.pkl")
        with pytest.raises(RuntimeError):
            qp.predict_proba(np.zeros((1, len(FEATURE_COLS))))


class TestAnomalyDetector:

    def test_fit_and_detect(self, tmp_path):
        rng = np.random.RandomState(42)
        X = rng.normal(size=(200, 5))
        det = AnomalyDetector(model_path=str(tmp_path / "an.pkl"),
                              contamination=0.1)
        metrics = det.fit(X)
        assert "anomaly_rate" in metrics
        labels = det.detect(X)
        assert set(np.unique(labels)).issubset({0, 1})

    def test_anomaly_rate_in_range(self, tmp_path):
        rng = np.random.RandomState(42)
        X = rng.normal(size=(200, 5))
        det = AnomalyDetector(model_path=str(tmp_path / "an.pkl"),
                              contamination=0.05)
        det.fit(X)
        labels = det.detect(X)
        rate = labels.mean()
        # نرخ ناهنجاری باید نزدیک به مقدار آلودگی تنظیم‌شده باشد
        assert 0.0 <= rate <= 0.3

    def test_save_and_load(self, tmp_path):
        rng = np.random.RandomState(42)
        X = rng.normal(size=(200, 5))
        path = str(tmp_path / "an.pkl")
        det = AnomalyDetector(model_path=path, contamination=0.05)
        det.fit(X)
        det2 = AnomalyDetector(model_path=path)
        labels1 = det.detect(X)
        labels2 = det2.detect(X)
        np.testing.assert_array_equal(labels1, labels2)


class TestEnergyPredictor:

    def test_fit_and_predict(self):
        rng = np.random.RandomState(42)
        X = rng.uniform(size=(100, 4))
        # قانون خطی: y = 2*x0 + 3*x1 - x2 + 1
        y = 2 * X[:, 0] + 3 * X[:, 1] - X[:, 2] + 1.0
        ep = EnergyPredictor()
        r2 = ep.fit(X, y)
        assert r2 > 0.9  # مدل خطی باید به‌خوبی برازش کند

    def test_predict_after_fit(self):
        rng = np.random.RandomState(42)
        X = rng.uniform(size=(100, 4))
        y = 2 * X[:, 0] + 3 * X[:, 1]
        ep = EnergyPredictor()
        ep.fit(X, y)
        pred = ep.predict(X[0])
        assert isinstance(pred, float)

    def test_predict_without_fit_raises(self):
        ep = EnergyPredictor()
        with pytest.raises(RuntimeError):
            ep.predict(np.zeros(4))


class TestCureOptimizer:

    def test_optimize_returns_dict(self, tmp_path):
        ht = HeatTransferModel()
        ck = CureKineticsModel()
        qp = QualityPredictor(model_path=str(tmp_path / "q.pkl"))
        X, y = _make_classification_data(100, 0.7)
        qp.fit(X, y)
        ep = EnergyPredictor()
        ep.fit(X[:, :4], np.zeros(100))
        opt = CureOptimizer(ht, ck, qp, ep)
        inp = CureCycleInput(
            press_id=1, tire_id=1, compound_code="CMP-A1",
            steam_pressure=1.5, hot_water_temp=170.0,
            nitrogen_pressure=1.2,
        )
        result = opt.optimize(inp)
        assert isinstance(result, dict)
        assert "optimal_time_min" in result
        assert "predicted_cure_degree" in result
        assert "predicted_quality_prob" in result
        assert "predicted_energy_kwh" in result
        assert "savings_vs_baseline_pct" in result

    def test_optimal_time_positive(self, tmp_path):
        ht = HeatTransferModel()
        ck = CureKineticsModel()
        qp = QualityPredictor(model_path=str(tmp_path / "q.pkl"))
        X, y = _make_classification_data(100, 0.7)
        qp.fit(X, y)
        opt = CureOptimizer(ht, ck, qp)
        inp = CureCycleInput(
            press_id=1, tire_id=1, compound_code="CMP-A1",
            steam_pressure=1.5, hot_water_temp=170.0,
            nitrogen_pressure=1.2,
        )
        result = opt.optimize(inp)
        assert result["optimal_time_min"] > 0

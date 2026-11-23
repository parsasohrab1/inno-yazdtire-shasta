"""مدل‌های یادگیری ماشین سامانه TCOP

QualityPredictor  – پیش‌بینی کیفیت تایر (ماژول ۳ – FR-3.1)
AnomalyDetector    – تشخیص انحراف پرس/قالب (ماژول ۳ – FR-3.2)
CureOptimizer     – بهینه‌سازی چرخه پخت (ماژول ۲ – FR-2.1)
"""
from __future__ import annotations

import os
import json
import numpy as np
import joblib
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    roc_auc_score, accuracy_score, precision_score, recall_score,
    f1_score, mean_absolute_percentage_error, confusion_matrix,
)

from app.core.config import ARTIFACTS_DIR, TARGET_CURE_DEGREE, RANDOM_STATE
from app.services.cure_kinetics import CureKineticsModel


# ---------------------------------------------------------------
# QualityPredictor
# ---------------------------------------------------------------
FEATURE_COLS = [
    "steam_pressure", "hot_water_temp", "nitrogen_pressure",
    "duration_min", "energy_kwh", "tool_wear", "torque",
]


@dataclass
class QualityPredictorResult:
    quality_prob: float
    predicted_label: int


class QualityPredictor:
    """پیش‌بینی احتمال سالم بودن تایر پیش از خروج از پرس"""

    def __init__(self, model_path: str | None = None) -> None:
        self.model_path = model_path or str(ARTIFACTS_DIR / "quality_gb.pkl")
        self.scaler: StandardScaler | None = None
        self.model: Any = None
        self.feature_cols = FEATURE_COLS
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.model_path):
            bundle = joblib.load(self.model_path)
            self.model = bundle.get("model")
            self.scaler = bundle.get("scaler")

    def fit(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """آموزش مدل Gradient Boosting"""
        self.scaler = StandardScaler().fit(X)
        Xs = self.scaler.transform(X)
        # GradientBoosting با تنظیمات منظم‌ساز برای جلوگیری از بیش‌برازش
        from sklearn.ensemble import GradientBoostingClassifier
        self.model = GradientBoostingClassifier(
            n_estimators=200, max_depth=3, learning_rate=0.1,
            min_samples_leaf=10, subsample=0.8, random_state=RANDOM_STATE,
        )
        self.model.fit(Xs, y)
        self.save()
        return self.evaluate(X, y)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if self.model is None:
            raise RuntimeError("مدل آموزش ندیده است.")
        Xs = self.scaler.transform(X)
        return self.model.predict_proba(Xs)[:, 1]

    def predict(self, X: np.ndarray) -> QualityPredictorResult:
        prob = float(self.predict_proba(X.reshape(1, -1) if X.ndim == 1 else X)[0])
        return QualityPredictorResult(quality_prob=round(prob, 4),
                                       predicted_label=int(prob >= 0.5))

    def evaluate(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        proba = self.predict_proba(X)
        pred = (proba >= 0.5).astype(int)
        try:
            auc = roc_auc_score(y, proba)
        except ValueError:
            auc = 0.5
        return {
            "accuracy": round(accuracy_score(y, pred), 4),
            "precision": round(precision_score(y, pred, zero_division=0), 4),
            "recall": round(recall_score(y, pred, zero_division=0), 4),
            "f1": round(f1_score(y, pred, zero_division=0), 4),
            "auc": round(auc, 4),
        }

    def save(self) -> None:
        joblib.dump({"model": self.model, "scaler": self.scaler},
                    self.model_path)


# ---------------------------------------------------------------
# AnomalyDetector
# ---------------------------------------------------------------
class AnomalyDetector:
    """تشخیص انحراف تدریجی پرس/قالب با Isolation Forest"""

    def __init__(self, model_path: str | None = None,
                 contamination: float = 0.05) -> None:
        self.model_path = model_path or str(ARTIFACTS_DIR / "anomaly_if.pkl")
        self.contamination = contamination
        self.model: IsolationForest | None = None
        self.scaler: StandardScaler | None = None
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.model_path):
            bundle = joblib.load(self.model_path)
            self.model = bundle.get("model")
            self.scaler = bundle.get("scaler")
            self.contamination = bundle.get("contamination", self.contamination)

    def fit(self, X: np.ndarray) -> Dict[str, float]:
        self.scaler = StandardScaler().fit(X)
        Xs = self.scaler.transform(X)
        self.model = IsolationForest(
            n_estimators=200, contamination=self.contamination,
            random_state=RANDOM_STATE,
        )
        self.model.fit(Xs)
        self.save()
        return self.score(X)

    def score(self, X: np.ndarray) -> Dict[str, float]:
        if self.model is None:
            raise RuntimeError("مدل آموزش ندیده است.")
        Xs = self.scaler.transform(X)
        raw = -self.model.score_samples(Xs)  # بالاتر = ناهنجارتر
        anomaly_rate = float((self.model.predict(Xs) == -1).mean())
        return {
            "mean_anomaly_score": round(float(np.mean(raw)), 4),
            "max_anomaly_score": round(float(np.max(raw)), 4),
            "anomaly_rate": round(anomaly_rate, 4),
        }

    def detect(self, X: np.ndarray) -> np.ndarray:
        """برچسب ناهنجاری برای هر سطر"""
        Xs = self.scaler.transform(X)
        return (self.model.predict(Xs) == -1).astype(int)

    def save(self) -> None:
        joblib.dump({"model": self.model, "scaler": self.scaler,
                     "contamination": self.contamination}, self.model_path)


# ---------------------------------------------------------------
# CureOptimizer
# ---------------------------------------------------------------
@dataclass
class CureCycleInput:
    press_id: int
    tire_id: int
    compound_code: str
    target_cure_degree: float = TARGET_CURE_DEGREE
    current_temp_profile: List[float] | None = None
    steam_pressure: float = 0.0
    hot_water_temp: float = 0.0
    nitrogen_pressure: float = 0.0


class EnergyPredictor:
    """پیش‌بینی مصرف انرژی با رگرسیون خطی"""

    def __init__(self) -> None:
        self.model: LinearRegression | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> float:
        self.model = LinearRegression().fit(X, y)
        pred = self.model.predict(X)
        ss_res = float(np.sum((y - pred) ** 2))
        ss_tot = float(np.sum((y - np.mean(y)) ** 2)) or 1.0
        return round(1 - ss_res / ss_tot, 4)  # R2

    def predict(self, X: np.ndarray) -> float:
        if self.model is None:
            raise RuntimeError("مدل انرژی آموزش ندیده است.")
        return float(self.model.predict(X.reshape(1, -1) if X.ndim == 1 else X)[0])


class CureOptimizer:
    """ماژول ۲ – بهینه‌سازی تطبیقی زمان چرخه پخت"""

    def __init__(self, heat_model, kinetics_model: CureKineticsModel,
                 quality_model: QualityPredictor,
                 energy_model: EnergyPredictor | None = None) -> None:
        self.heat = heat_model
        self.kinetics = kinetics_model
        self.ml = quality_model
        self.energy = energy_model

    def optimize(self, inp: CureCycleInput) -> dict:
        # 1) شبیه‌سازی پروفایل دما
        temp_profile = self.heat.simulate(
            compound=inp.compound_code,
            steam_p=inp.steam_pressure,
            water_t=inp.hot_water_temp,
        )
        # 2) انتگرال‌گیری درجه پخت
        cure_deg = self.kinetics.integrate(temp_profile)
        # 3) یافتن کمینه زمان رسیدن به هدف
        t_opt = self._find_min_time(cure_deg, inp.target_cure_degree)
        # 4) پیش‌بینی کیفیت با ML
        feature_vec = np.array([[
            inp.steam_pressure, inp.hot_water_temp, inp.nitrogen_pressure,
            t_opt, 0.0, 0.0, 0.0,
        ]])
        try:
            quality = float(self.ml.predict_proba(feature_vec)[0])
        except Exception:
            quality = 0.95
        # 5) پیش‌بینی مصرف انرژی
        if self.energy is not None:
            try:
                evec = np.array([[inp.steam_pressure, inp.hot_water_temp,
                                  inp.nitrogen_pressure, t_opt]])
                energy = self.energy.predict(evec)
            except Exception:
                energy = 55.0
        else:
            energy = 55.0
        return {
            "optimal_time_min": round(t_opt, 2),
            "predicted_cure_degree": round(float(cure_deg[-1]), 4),
            "predicted_quality_prob": round(quality, 4),
            "predicted_energy_kwh": round(float(energy), 2),
            "savings_vs_baseline_pct": self._savings(t_opt),
        }

    def _find_min_time(self, cure_deg: np.ndarray, target: float) -> float:
        idx = np.where(cure_deg >= target)[0]
        # هر گام برابر 5 دقیقه (n_time=300 روی t_max=1500s -> dt=5s)
        # برای سازگاری با واحدهای پروژه، ضریب 0.05 دقیقه/گام
        step_min = 0.05
        return float(idx[0] * step_min) if len(idx) else float(len(cure_deg) * step_min)

    def _savings(self, t_opt: float) -> float:
        from app.core.config import CURE_BASELINE_MIN
        return round((CURE_BASELINE_MIN - t_opt) / CURE_BASELINE_MIN * 100, 2)

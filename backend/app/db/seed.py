"""تولید و درج داده‌های مصنوعی مطابق بخش ۶.۲ SRS (تطبیق‌یافته برای SQLite)"""
from __future__ import annotations

import random
import json
from datetime import datetime, timedelta, date


def _d(s):
    if isinstance(s, date):
        return s
    if not s:
        return None
    try:
        return datetime.strptime(str(s)[:10], "%Y-%m-%d").date()
    except Exception:
        return None

from sqlalchemy import text

from app.db.session import session_scope
from app.core.config import RANDOM_STATE

random.seed(RANDOM_STATE)


PRESS_COUNT = 15
COMPOUND_ROWS = [
    {"code": "CMP-A1", "name": "Tread Compound A1",
     "spec_json": {"density": 1.15, "k": 0.25}},
    {"code": "CMP-B2", "name": "Sidewall Compound B2",
     "spec_json": {"density": 1.10, "k": 0.22}},
    {"code": "CMP-C3", "name": "Inner Liner C3",
     "spec_json": {"density": 1.20, "k": 0.28}},
]
TIRE_COUNT = 100
MOLD_COUNT = 30
CYCLE_COUNT = 2000
QUALITY_TESTS_PER_TIRE = 3


def _rand_float(a: float, b: float, ndigits: int = 2):
    return round(random.uniform(a, b), ndigits)


def generate_presses():
    return [{"name": f"Press-{i:02d}", "model": "YZ-2000",
             "status": "active", "installed_at": _d("2020-01-01")}
            for i in range(1, PRESS_COUNT + 1)]


def generate_compounds():
    return COMPOUND_ROWS


def generate_tires():
    out = []
    codes = [c["code"] for c in COMPOUND_ROWS]
    for i in range(1, TIRE_COUNT + 1):
        out.append({
            "code": f"TIRE-{i:04d}",
            "compound_code": random.choice(codes),
            "structure_json": {"width": 205, "ratio": 55, "rim": 16, "layers": 4},
        })
    return out


def generate_molds():
    return [{"code": f"MOLD-{i:03d}", "press_id": i % PRESS_COUNT + 1,
             "status": "ok", "total_cycles": random.randint(0, 5000),
             "last_service": _d("2024-06-01")} for i in range(1, MOLD_COUNT + 1)]


def generate_cycles_and_predictions():
    """ساخت چرخه‌های پخت + سنسورها + پیش‌بینی‌ها به‌صورت هماهنگ"""
    cycles, sensors, preds = [], [], []
    base = datetime(2025, 1, 1)
    for i in range(1, CYCLE_COUNT + 1):
        press_id = random.randint(1, PRESS_COUNT)
        tire_id = random.randint(1, TIRE_COUNT)
        mold_id = random.randint(1, MOLD_COUNT)
        start = base + timedelta(minutes=i * 25)
        dur = random.uniform(18.0, 26.0)
        end = start + timedelta(minutes=dur)
        steam = _rand_float(1.2, 1.8, 3)
        water = _rand_float(160, 180, 2)
        nitro = _rand_float(1.0, 1.4, 3)
        # انرژی تابع فیزیکی واقعی: P = U * I * t -> مرتبط با فشار، دما و مدت
        # مقیاس‌بندی مجدد برای قرارگیری در محدوده ۳۰-۷۵ kWh
        energy_raw = (
            10.0
            + 12.0 * (steam - 1.2) / 0.6     # فشار بخار → انرژی بخار
            + 0.15 * (water - 160)          # دمای آب → گرمایش
            + 0.6 * (dur - 18)              # مدت → مصرف مستقیم
            + 5.0 * (nitro - 1.0) / 0.4     # فشار نیتروژن → انرژی فشرده‌سازی
        )
        energy = round(max(20.0, min(80.0,
            energy_raw + random.uniform(-2.0, 2.0))), 2)
        cycles.append({
            "press_id": press_id, "tire_id": tire_id, "mold_id": mold_id,
            "start_ts": start, "end_ts": end,
            "duration_min": round(dur, 2),
            "steam_pressure": steam, "hot_water_temp": water,
            "nitrogen_pressure": nitro, "energy_kwh": energy,
            "source": "synthetic",
        })
        for t in range(10):
            sensors.append({
                "time": start + timedelta(minutes=t * dur / 10),
                "press_id": press_id, "sensor": "temp",
                "value": round(150 + random.uniform(-8, 8), 2),
            })
        # درجه پخت تابعی فیزیکی‌تر از دما و زمان (نه کاملاً تصادفی)
        cure_deg = min(1.0, max(0.0,
            0.7 + 0.02 * (water - 170) + 0.01 * (dur - 22) + random.uniform(-0.03, 0.03)))
        # کیفیت وابسته به ویژگی‌های فرآیند (برای یادپذیری مدل ML)
        # نمره کیفی پایه از فشار بخار و دما
        # میانگین تنظیم شده تا تقریباً نیمی از نمونه‌ها از آستانه ۰.۸۵ عبور کنند
        base_q = (0.55
                  + 0.30 * (steam - 1.2) / 0.6     # فشار بالاتر = پخت بهتر
                  + 0.20 * (water - 160) / 20      # دمای بالاتر = پخت بهتر
                  - 0.15 * abs(dur - 22) / 4       # انحراف از زمان مطلوب = افت کیفیت
                  + 0.10 * (nitro - 1.0) / 0.4)    # فشار نیتروژن مناسب
        # تزریق نویز واقعی (نویز متوسط برای جلوگیری از بیش‌برازش)
        quality = max(0.4, min(0.99, base_q + random.uniform(-0.05, 0.05)))
        # انحراف/آنومالی تابع انحراف فرآیند از حالت ایده‌آل
        anomaly = max(0.0, min(0.9,
            0.05
            + 0.30 * abs(steam - 1.5) / 0.3
            + 0.20 * abs(water - 170) / 10
            + 0.10 * abs(dur - 22) / 4
            + random.uniform(-0.02, 0.05)))
        preds.append({
            "cure_cycle_id": i, "cure_degree": round(cure_deg, 4),
            "quality_prob": round(quality, 4),
            "anomaly_score": round(anomaly, 4),
            "model_version": "synthetic-v1.0",
        })
    return cycles, sensors, preds


def generate_quality_tests():
    qts = []
    for tire_id in range(1, TIRE_COUNT + 1):
        for j in range(QUALITY_TESTS_PER_TIRE):
            passed = random.random() > 0.15
            qts.append({
                "tire_id": tire_id, "test_type": "uniformity",
                "result_json": {"radial": round(random.uniform(0, 5), 2),
                                "lateral": round(random.uniform(0, 5), 2)},
                "passed": passed,
            })
    return qts


def insert_rows(session, table: str, rows: list[dict], model_cls) -> int:
    if not rows:
        return 0
    objs = [model_cls(**r) for r in rows]
    session.add_all(objs)
    session.flush()
    return len(objs)


def load_synthetic_data(verbose: bool = True) -> dict:
    """بارگذاری کامل داده‌های مصنوعی در پایگاه داده"""
    from app.models.orm import (
        Press, Compound, Tire, Mold, CureCycle, SensorReading,
        QualityTest, Prediction, User,
    )

    presses = generate_presses()
    compounds = generate_compounds()
    tires_raw = generate_tires()
    molds = generate_molds()
    cycles, sensors, preds = generate_cycles_and_predictions()
    qts = generate_quality_tests()

    counts = {}
    with session_scope() as s:
        counts["presses"] = insert_rows(s, "presses", presses, Press)
        counts["compounds"] = insert_rows(s, "compounds", compounds, Compound)

        # نگاشت کد آمیزه به id
        comp_map = {c.code: c.id for c in s.query(Compound).all()}
        tires = []
        for t in tires_raw:
            tire = Tire(code=t["code"],
                         compound_id=comp_map[t["compound_code"]],
                         structure_json=t["structure_json"])
            tires.append(tire)
            s.add(tire)
        s.flush()
        counts["tires"] = len(tires)

        counts["molds"] = insert_rows(s, "molds", molds, Mold)
        counts["cure_cycles"] = insert_rows(s, "cure_cycles", cycles, CureCycle)
        counts["sensor_readings"] = insert_rows(s, "sensor_readings",
                                                sensors, SensorReading)
        counts["quality_tests"] = insert_rows(s, "quality_tests", qts, QualityTest)
        counts["predictions"] = insert_rows(s, "predictions", preds, Prediction)

        # کاربر پیش‌فرض
        if not s.query(User).filter_by(username="admin").first():
            s.add(User(username="admin",
                       password_hash="pbkdf2:sha256$dummy",
                       role="admin", is_active=True))
            counts["users"] = 1
        else:
            counts["users"] = 0

    if verbose:
        print("✅ داده‌های مصنوعی با موفقیت درج شدند:")
        for k, v in counts.items():
            print(f"   {k}: {v}")
    return counts


if __name__ == "__main__":
    load_synthetic_data()

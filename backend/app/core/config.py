"""تنظیمات مرکزی سامانه TCOP"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
SYNTHETIC_DIR = DATA_DIR / "synthetic"
ARTIFACTS_DIR = BASE_DIR / "backend" / "app" / "ml" / "artifacts"

# پایگاه داده SQLite برای اجرای آسان محیط آزمایشگاهی (جایگزین PostgreSQL)
DB_PATH = BASE_DIR / "backend" / "tcop.db"
DATABASE_URL = os.getenv("TCOP_DATABASE_URL", f"sqlite:///{DB_PATH}")

# پارامترهای فرآیند پخت (استاندارد یزد تایر – مقادیر مرجع)
CURE_BASELINE_MIN = 22.0          # زمان چرخه پایه (دقیقه)
TARGET_CURE_DEGREE = 0.90          # حداقل درجه پخت قابل‌قبول
STEAM_PRESSURE_RANGE = (1.2, 1.8)  # بار
HOT_WATER_TEMP_RANGE = (160, 180)  # درجه سانتی‌گراد
NITROGEN_RANGE = (1.0, 1.4)        # بار

# پارامترهای مدل ML
RANDOM_STATE = 42
TEST_SIZE = 0.2

# مسیر داده‌های واقعی
AI4I_CSV = RAW_DIR / "ai4i2020_real.csv"
SECOM_DATA = RAW_DIR / "secom_dir" / "secom.data"
SECOM_LABELS = RAW_DIR / "secom_dir" / "secom_labels.data"


for d in (DATA_DIR, RAW_DIR, PROCESSED_DIR, SYNTHETIC_DIR,
          ARTIFACTS_DIR, ARTIFACTS_DIR.parent):
    d.mkdir(parents=True, exist_ok=True)

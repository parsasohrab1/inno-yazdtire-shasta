"""تست‌های واحد پیکربندی سامانه"""
import pytest
from pathlib import Path

from app.core.config import (
    BASE_DIR, DATA_DIR, RAW_DIR, PROCESSED_DIR, SYNTHETIC_DIR,
    ARTIFACTS_DIR, DB_PATH, DATABASE_URL,
    CURE_BASELINE_MIN, TARGET_CURE_DEGREE,
    STEAM_PRESSURE_RANGE, HOT_WATER_TEMP_RANGE, NITROGEN_RANGE,
    RANDOM_STATE, TEST_SIZE,
    AI4I_CSV, SECOM_DATA, SECOM_LABELS,
)


class TestConfig:

    def test_paths_exist(self):
        assert DATA_DIR.exists()
        assert RAW_DIR.exists()
        assert PROCESSED_DIR.exists()
        assert SYNTHETIC_DIR.exists()
        assert ARTIFACTS_DIR.exists()

    def test_database_url_is_sqlite(self):
        assert DATABASE_URL.startswith("sqlite:///")

    def test_cure_baseline(self):
        assert CURE_BASELINE_MIN == 22.0

    def test_target_cure_degree(self):
        assert 0 < TARGET_CURE_DEGREE <= 1.0

    def test_ranges_valid(self):
        assert STEAM_PRESSURE_RANGE[0] < STEAM_PRESSURE_RANGE[1]
        assert HOT_WATER_TEMP_RANGE[0] < HOT_WATER_TEMP_RANGE[1]
        assert NITROGEN_RANGE[0] < NITROGEN_RANGE[1]

    def test_random_state_consistent(self):
        assert RANDOM_STATE == 42

    def test_test_size(self):
        assert 0 < TEST_SIZE < 1


class TestRealDataPaths:

    def test_ai4i_csv_exists(self):
        """داده واقعی AI4I باید در مسیر مشخص باشد"""
        assert AI4I_CSV.exists(), f"فایل AI4I یافت نشد: {AI4I_CSV}"

    def test_secom_data_exists(self):
        assert SECOM_DATA.exists(), f"فایل SECOM یافت نشد: {SECOM_DATA}"

    def test_secom_labels_exist(self):
        assert SECOM_LABELS.exists()

"""تست‌های واحد مدل سینتیک پخت"""
import numpy as np
import pytest

from app.services.cure_kinetics import CureKineticsModel


class TestCureKineticsModel:

    def test_default_params(self):
        ck = CureKineticsModel()
        assert ck.Ea == 80000.0
        assert ck.k0 == 1e10
        assert ck.n == 1.5
        assert ck.R == 8.314

    def test_rate_positive(self):
        ck = CureKineticsModel()
        r = ck.rate(T_kelvin=400.0, cure=0.0)
        assert r > 0  # نرخ پخت مثبت است

    def test_rate_decreases_with_cure(self):
        ck = CureKineticsModel()
        r1 = ck.rate(T_kelvin=400.0, cure=0.0)
        r2 = ck.rate(T_kelvin=400.0, cure=0.5)
        assert r2 < r1  # هرچه پخت بیشتر، نرخ کمتر

    def test_rate_increases_with_temp(self):
        ck = CureKineticsModel()
        r_cold = ck.rate(T_kelvin=350.0, cure=0.0)
        r_hot = ck.rate(T_kelvin=450.0, cure=0.0)
        assert r_hot > r_cold  # دمای بالاتر = نرخ پخت بیشتر

    def test_integrate_returns_array(self):
        ck = CureKineticsModel()
        temp_profile = np.array([100.0, 120.0, 150.0, 170.0, 170.0])
        cure = ck.integrate(temp_profile, dt=1.0)
        assert isinstance(cure, np.ndarray)
        assert len(cure) == len(temp_profile)

    def test_integrate_monotonic_non_decreasing(self):
        """درجه پخت باید نافزاینده باشد"""
        ck = CureKineticsModel()
        temp_profile = np.full(50, 170.0)
        cure = ck.integrate(temp_profile, dt=1.0)
        diffs = np.diff(cure)
        assert np.all(diffs >= -1e-10)  # نافزاینده

    def test_integrate_bounded(self):
        """درجه پخت باید در بازه [۰, ۱] باشد"""
        ck = CureKineticsModel()
        temp_profile = np.full(100, 200.0)
        cure = ck.integrate(temp_profile, dt=5.0)
        assert np.all(cure >= 0)
        assert np.all(cure <= 1.0)

    def test_time_to_target(self):
        ck = CureKineticsModel()
        temp_profile = np.full(200, 170.0)
        t = ck.time_to_target(temp_profile, target=0.5, dt=1.0)
        assert t > 0
        assert isinstance(t, float)

    def test_time_to_target_unreachable(self):
        """اگر دما بسیار پایین باشد و درجه پخت به هدف نرسد"""
        ck = CureKineticsModel()
        temp_profile = np.full(10, 30.0)  # دمای محیط
        t = ck.time_to_target(temp_profile, target=0.9, dt=1.0)
        # باید کل طول پروفایل برگردد
        assert t > 0

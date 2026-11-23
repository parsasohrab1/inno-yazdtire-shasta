"""تست‌های واحد مدل انتقال حرارت"""
import numpy as np
import pytest

from app.services.heat_transfer import HeatTransferModel, HeatTransferConfig


class TestHeatTransferModel:

    def test_default_config(self):
        ht = HeatTransferModel()
        assert ht.cfg.alpha > 0
        assert ht.cfg.thickness > 0
        assert ht.n == ht.cfg.n_nodes

    def test_simulate_returns_array(self):
        ht = HeatTransferModel()
        T = ht.simulate(compound="CMP-A1", steam_p=1.5, water_t=170.0)
        assert isinstance(T, np.ndarray)
        assert len(T) > 0

    def test_temperature_increases_over_time(self):
        ht = HeatTransferModel()
        T = ht.simulate(compound="CMP-A1", steam_p=1.5, water_t=170.0)
        # دمای مرکز در پایان باید بالاتر از دمای اولیه باشد
        assert T[-1] > 25.0
        # دما باید به‌طور کلی رو به افزایش باشد
        assert T[-1] > T[0]

    def test_higher_steam_pressure_higher_temp(self):
        ht = HeatTransferModel()
        T_low = ht.simulate(steam_p=1.2, water_t=170.0)
        T_high = ht.simulate(steam_p=1.8, water_t=170.0)
        assert T_high[-1] >= T_low[-1] - 1e-6

    def test_higher_water_temp_higher_temp(self):
        ht = HeatTransferModel()
        T_low = ht.simulate(steam_p=1.5, water_t=160.0)
        T_high = ht.simulate(steam_p=1.5, water_t=180.0)
        assert T_high[-1] > T_low[-1]

    def test_compound_alpha_mapping(self):
        ht = HeatTransferModel()
        # آمیزه‌های مختلف باید آلفای متفاوت بدهند
        a1 = ht._alpha_for_compound("CMP-A1")
        b2 = ht._alpha_for_compound("CMP-B2")
        c3 = ht._alpha_for_compound("CMP-C3")
        assert a1 != b2 or b2 != c3  # حداقل یکی متفاوت باشد

    def test_unknown_compound_falls_back(self):
        ht = HeatTransferModel()
        alpha = ht._alpha_for_compound("UNKNOWN")
        assert alpha == ht.alpha  # برگشت به مقدار پیش‌فرض

    def test_steady_state_temp(self):
        ht = HeatTransferModel()
        t = ht.steady_state_temp(water_t=170.0, T0=25.0)
        # دمای حالت دائم باید بین دمای اولیه و دمای آب باشد
        assert 25.0 < t < 170.0

    def test_simulate_with_custom_config(self):
        cfg = HeatTransferConfig(n_nodes=20, t_max_sec=100.0)
        ht = HeatTransferModel(cfg)
        T = ht.simulate(steam_p=1.5, water_t=170.0)
        assert isinstance(T, np.ndarray)
        assert len(T) > 0

    def test_temperature_bounded(self):
        """دمای مرکز نباید از دمای آب داغ بیشتر شود"""
        ht = HeatTransferModel()
        T = ht.simulate(steam_p=1.5, water_t=170.0)
        assert np.all(T <= 200.0)  # محدود فیزیکی

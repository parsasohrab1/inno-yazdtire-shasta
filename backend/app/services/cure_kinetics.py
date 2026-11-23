"""سینتیک پخت بر اساس معادله آرنیوس (ماژول ۱ – FR-1.4)

مدل پخت لاستیک با معادله نطفه‌بستن نرمال‌شده ن猝n:
    dc/dt = k(T) * (1 - c)^n
    k(T) = k0 * exp(-Ea / (R * T))
"""
from __future__ import annotations

import numpy as np


class CureKineticsModel:
    """سینتیک پخت لاستیک"""

    R = 8.314  # J/(mol.K)

    def __init__(self, Ea: float = 80000.0, k0: float = 1e10, n: float = 1.5) -> None:
        self.Ea = Ea          # انرژی فعال‌سازی (J/mol)
        self.k0 = k0           # فاکتور پیش‌نمایی
        self.n = n              # مرتبه واکنش

    def rate(self, T_kelvin: float, cure: float) -> float:
        """نرخ لحظه‌ای پخت"""
        k = self.k0 * np.exp(-self.Ea / (self.R * T_kelvin))
        return float(k * (1.0 - cure) ** self.n)

    def integrate(self, temp_profile: np.ndarray, dt: float = 1.0) -> np.ndarray:
        """انتگرال‌گیری زمانی درجه پخت از پروفایل دما (سانی‌گراد).

        خروجی: آرایه‌ای از مقادیر درجه پخت در طول زمان.
        """
        temp_profile = np.asarray(temp_profile, dtype=float)
        cure = np.zeros(len(temp_profile))
        for i in range(1, len(temp_profile)):
            T = temp_profile[i] + 273.15
            cure[i] = cure[i - 1] + self.rate(T, cure[i - 1]) * dt
            cure[i] = min(cure[i], 1.0)
        return cure

    def time_to_target(self, temp_profile: np.ndarray, target: float = 0.9,
                      dt: float = 1.0) -> float:
        """زمان رسیدن به درجه پخت هدف (دقیقه)"""
        cure = self.integrate(temp_profile, dt=dt)
        idx = np.where(cure >= target)[0]
        return float(idx[0] * dt / 60.0) if len(idx) else float(len(cure) * dt / 60.0)

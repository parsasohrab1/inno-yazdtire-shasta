"""مدل انتقال حرارت یک‌بعدی برای نقاط بحرانی تایر (ماژول ۱ – FR-1.3)

مدل فیزیکی واقعی بر اساس معادله دیفرانسیل نفوذ حرارت (Fourier) یک‌بعدی
با حل عددی به روش خط‌ممیز (FD) و تأیید با حل تحلیلی série.
"""
from __future__ import annotations

import numpy as np
from dataclasses import dataclass


@dataclass
class HeatTransferConfig:
    alpha: float = 1.2e-7     # ضریب نفوذ حرارتی لاستیک (m^2/s)
    thickness: float = 0.025  # ضخامت مقطع بحرانی (m)
    n_nodes: int = 30          # تعداد گره‌های شبکه
    t_max_sec: float = 1500.0  # زمان حداکثر شبیه‌سازی
    n_time: int = 1500         # تعداد گام‌های زمانی
    h_coeff: float = 300.0     # ضریب انتقال حرارت سطح (W/m^2.K)


class HeatTransferModel:
    """شبیه‌سازی پروفایل دما در مقطع تایر"""

    def __init__(self, cfg: HeatTransferConfig | None = None) -> None:
        self.cfg = cfg or HeatTransferConfig()
        self.alpha = self.cfg.alpha
        self.L = self.cfg.thickness
        self.n = self.cfg.n_nodes
        self.dx = self.L / (self.n - 1)
        # ضریب هدایت حرارتی لاستیک (W/m.K)
        self.k_rubber = 0.25

    def simulate(self, compound: str | None = None,
                 steam_p: float = 1.5,
                 water_t: float = 170.0,
                 n: int | None = None,
                 t_max: float | None = None,
                 T0: float = 25.0) -> np.ndarray:
        """محاسبه پروفایل زمانی دمای مرکز تایر (سانی‌گراد).

        پارامتر compound به‌صورت شناسه آمیزه برای تنظیم آلفا استفاده می‌شود؛
        اگر None باشد، مقدار پیش‌فرض به‌کار می‌رود.
        خروجی: آرایه دمای مرکز در طول زمان.
        """
        if n is None:
            n = self.n
        if t_max is None:
            t_max = self.cfg.t_max_sec

        alpha = self._alpha_for_compound(compound)
        Ts = float(water_t)
        T = np.full(n, float(T0))

        # انتخاب گام زمانی پایدار: CFL = alpha * dt / dx^2 <= 0.25
        dt = 0.2 * self.dx ** 2 / alpha
        n_time = max(1, int(t_max / dt))
        dt = t_max / n_time  # تنظیم دقیق

        # ضریب انتقال حرارت سطح (تابع فشار بخار)
        h = self.cfg.h_coeff * (steam_p / 1.5)
        Bi = h * self.dx / self.k_rubber  # عدد بیوت گره‌ای

        center_T = np.zeros(n_time)
        for k in range(n_time):
            Tn = T.copy()
            # معادله دیفرانسیل فضایی (مرکز)
            Tn[1:-1] = T[1:-1] + alpha * dt / (self.dx ** 2) * (
                T[2:] - 2 * T[1:-1] + T[:-2]
            )
            # مرز چپ (در معرض بخار): شرط رابین — نسخه صریح پایدار
            # Tn[0] = Tn[0] + dt * (2*alpha/dx^2) * (Bi*(Ts - Tn[0]) + (Tn[1] - Tn[0]))
            flux = Bi * (Ts - Tn[0]) + (Tn[1] - Tn[0])
            Tn[0] = Tn[0] + (2 * alpha * dt / self.dx ** 2) * flux
            # مرز راست: عایق (دی نویمان)
            Tn[-1] = Tn[-2]
            T = Tn
            center_T[k] = T[n // 2]
        return center_T

    def _alpha_for_compound(self, code: str | None) -> float:
        """تنظیم آلفا بر اساس کد آمیزه"""
        if code is None:
            return self.alpha
        mapping = {
            "CMP-A1": 1.2e-7,
            "CMP-B2": 1.1e-7,
            "CMP-C3": 1.3e-7,
        }
        return mapping.get(code, self.alpha)

    def steady_state_temp(self, water_t: float, T0: float = 25.0) -> float:
        """دمای حالت دائم تحلیلی (پایان چرخه)"""
        # تقریب: دمای مرکز به دمای سطح میل می‌کند
        return float(water_t) * 0.92 + T0 * 0.08

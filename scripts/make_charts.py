"""Generate charts for the ML training & coverage report (Persian labels)."""
import matplotlib.font_manager as fm
fm.fontManager.addfont('/home/z/my-project/scripts/fonts/Amiri-Regular.ttf')
fm.fontManager.addfont('/home/z/my-project/scripts/fonts/Amiri-Bold.ttf')
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
import matplotlib.pyplot as plt
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display

def fa(s):
    """Reshape + bidi for proper Persian rendering in matplotlib."""
    return get_display(arabic_reshaper.reshape(s))

plt.rcParams['font.family'] = 'Amiri'
plt.rcParams['axes.unicode_minus'] = False

OUT = '/home/z/my-project/download/_charts'
import os; os.makedirs(OUT, exist_ok=True)

# Palette DM-1 dark cyan accents
ACC = '#1B6B7A'; ACC2 = '#37DCF2'; SURF = '#EDF3F5'

# --- Chart 1: model accuracy & AUC across data sources ---
fig, ax = plt.subplots(figsize=(8, 4.2), constrained_layout=True)
groups = [fa('داده واقعی (AI4I)'), fa('داده مصنوعی'), fa('SECOM (نیمه‌هادی)')]
acc = [97.5, 92.5, 96.49]
auc = [97.85, 98.02, 99.81]
x = np.arange(len(groups)); w = 0.36
b1 = ax.bar(x - w/2, acc, w, label=fa('دقت (Accuracy)'), color=ACC)
b2 = ax.bar(x + w/2, auc, w, label=fa('AUC'), color=ACC2)
ax.axhline(90, color='#C0392B', ls='--', lw=1.2, label=fa('آستانه هدف ۹۰٪'))
ax.set_xticks(x); ax.set_xticklabels(groups, fontsize=10)
ax.set_ylabel(fa('درصد'), fontsize=11); ax.set_ylim(60, 105)
ax.set_title(fa('مقایسه دقت و AUC مدل‌های تشخیص کیفیت لاستیک'), fontsize=12, fontweight='bold')
for b in list(b1)+list(b2):
    ax.annotate(f'{b.get_height():.1f}', (b.get_x()+b.get_width()/2, b.get_height()),
                textcoords='offset points', xytext=(0,4), ha='center', fontsize=9)
ax.legend(loc='lower right', fontsize=9, ncol=3)
ax.grid(axis='y', alpha=0.3)
plt.savefig(f'{OUT}/chart_accuracy.png', dpi=130)
plt.close()
print('chart_accuracy saved')

# --- Chart 2: per-module test coverage ---
mods = [
    ('core/config', 100), ('models/orm', 100),
    ('services/cure_kinetics', 100), ('services/heat_transfer', 100),
    ('services/ml_models', 95), ('db/load_real', 92), ('db/seed', 92),
    ('db/session', 72),
]
mods.sort(key=lambda t: t[1])
names = [fa(m[0]) for m in mods]; vals = [m[1] for m in mods]
fig, ax = plt.subplots(figsize=(8, 4.4), constrained_layout=True)
colors = ['#C0392B' if v < 80 else ACC for v in vals]
bars = ax.barh(names, vals, color=colors)
ax.axvline(80, color='#E67E22', ls='--', lw=1.2, label=fa('آستانه هدف ۸۰٪'))
ax.axvline(94.2, color=ACC2, ls='--', lw=1.2, label=fa('میانگین کل ۹۴.۲٪'))
ax.set_xlabel(fa('درصد پوشش خط'), fontsize=11); ax.set_xlim(0, 108)
ax.set_title(fa('پوشش تست به تفکیک ماژول (۹۰ تست، ۰ شکست)'), fontsize=12, fontweight='bold')
for b, v in zip(bars, vals):
    ax.annotate(f'{v}%', (v, b.get_y()+b.get_height()/2),
                textcoords='offset points', xytext=(4,0), va='center', fontsize=9)
ax.legend(loc='lower right', fontsize=9)
ax.grid(axis='x', alpha=0.3)
plt.savefig(f'{OUT}/chart_coverage.png', dpi=130)
plt.close()
print('chart_coverage saved')

# --- Chart 3: additional ML metrics (anomaly / energy / physics) ---
fig, axes = plt.subplots(1, 3, figsize=(10, 3.6), constrained_layout=True)
# anomaly rate
ax = axes[0]
ax.bar([fa('واقعی'),fa('مصنوعی')], [5.0,5.0], color=ACC)
ax.set_title(fa('نرخ ناهنجاری شناسایی‌شده'), fontsize=10, fontweight='bold')
ax.set_ylabel(fa('درصد')); ax.set_ylim(0,8)
# energy R2
ax = axes[1]
ax.bar([fa('واقعی'),fa('مصنوعی')], [100, 84.31], color=[ACC, ACC2])
ax.set_title(fa('R² مدل مصرف انرژی'), fontsize=10, fontweight='bold')
ax.set_ylabel(fa('٪')); ax.set_ylim(0,108)
# physics MAPE
ax = axes[2]
ax.bar([fa('واقعی'),fa('مصنوعی')], [15.29, 45.97], color=[ACC, ACC2])
ax.set_title(fa('MAPE مدل سینتیک پخت (٪)'), fontsize=10, fontweight='bold')
ax.set_ylabel(fa('درصد خطا')); ax.set_ylim(0,55)
plt.savefig(f'{OUT}/chart_aux.png', dpi=130)
plt.close()
print('chart_aux saved')

# verify non-blank
from PIL import Image
for f in ['chart_accuracy','chart_coverage','chart_aux']:
    im=Image.open(f'{OUT}/{f}.png').convert('L'); h=im.histogram()
    print(f, im.size, 'non-white', round(1-h[255]/sum(h),3))

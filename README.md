# inno-yazdtire-shasta
# 🏭 سند جامع توسعه محصول TCOP
## سامانه هوشمند بهینه‌سازی چرخه پخت و پیش‌بینی کیفیت تایر

---

بر اساس نامه شرکت پتروپالاتوس به شرکت یزد تایر (شماره ۱۴۰۵۰۹۰۲۰۰۱ مورخ ۱۴۰۵/۰۹/۰۲)، سند جامع توسعه محصول TCOP در سطح **بلوغ ۴ (TRL-4 / Maturity Level 4 – Validation in Lab Environment)** تهیه شده است. این سند شامل اسکفلد پروژه (Project Scaffold)، کدنویسی تمامی ردیف‌های داده (Data Rows)، SRS، BRS، README، معماری Full-Stack، طراحی UI و نمودارهای محصول است.

---

# 📋 فهرست مطالب

1. [خلاصه اجرایی](#1)
2. [اسکفلد پروژه (Project Scaffold)](#2)
3. [BRS – سند نیازمندی‌های کسب‌وکار](#3)
4. [SRS – سند نیازمندی‌های نرم‌افزار + نمودارها](#4)
5. [معماری Full-Stack](#5)
6. [مدل داده و کدنویسی تمامی ردیف‌های داده](#6)
7. [طراحی UI/UX](#7)
8. [README – راهنمای پروژه](#8)
9. [نقشه راه بلوغ ۴](#9)

---

<a name="1"></a>
# ۱. خلاصه اجرایی

**TCOP (Tire Cure Optimization & Prediction)** یک سامانه هوشمند مبتنی بر هوش مصنوع، مدل‌سازی انتقال حرارت و سینتیک پخت است که برای شرکت یزد تایر طراحی شده تا:

- تخمین برخط میزان پخت در نقاط بحرانی تایر
- بهینه‌سازی تطبیقی زمان چرخه پخت و مصرف انرژی
- پیش‌بینی کیفیت تایر و تشخیص انحراف پرس/قالب
- پایش کیفیت آمیزه و فرآیند اختلاط

**سطح بلوغ هدف: ۴** — اعتبارسنجی در محیط آزمایشگاهی با داده‌های واقعی و شبیه‌سازی‌شده، آماده برای پایلوت صنعتی.

**تأمین بودجه:** اعتبار مالیاتی تحقیق و توسعه طبق بند «ب» ماده ۱۱ قانون جهش تولید دانش‌بنیان (مصوب ۱۴۰۱، اجرا از ۱۴۰۲) از طریق سامانه `www.etebar.ir`.

---

<a name="2"></a>
# ۲. اسکفلد پروژه (Project Scaffold)

## ۲.۱ ساختار پوشه‌ها

```
tcop/
├── README.md
├── docker-compose.yml
├── .env.example
├── Makefile
├── docs/
│   ├── BRS.md
│   ├── SRS.md
│   ├── architecture.md
│   ├── diagrams/
│   │   ├── context-diagram.png
│   │   ├── use-case.png
│   │   ├── er-diagram.png
│   │   ├── sequence-cure.png
│   │   ├── deployment.png
│   │   └── component.png
│   └── api/
│       └── openapi.yaml
├── backend/
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── logging.py
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── router.py
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── presses.py
│   │   │   │   │   ├── compounds.py
│   │   │   │   │   ├── tires.py
│   │   │   │   │   ├── cure_cycles.py
│   │   │   │   │   ├── molds.py
│   │   │   │   │   ├── quality.py
│   │   │   │   │   ├── predictions.py
│   │   │   │   │   ├── optimization.py
│   │   │   │   │   └── anomalies.py
│   │   │   │   └── deps.py
│   │   ├── models/           # SQLAlchemy ORM
│   │   │   ├── press.py
│   │   │   ├── compound.py
│   │   │   ├── tire.py
│   │   │   ├── cure_cycle.py
│   │   │   ├── mold.py
│   │   │   ├── quality_test.py
│   │   │   ├── prediction.py
│   │   │   └── user.py
│   │   ├── schemas/          # Pydantic
│   │   ├── services/
│   │   │   ├── heat_transfer.py
│   │   │   ├── cure_kinetics.py
│   │   │   ├── ml_models.py
│   │   │   ├── optimizer.py
│   │   │   ├── anomaly_detector.py
│   │   │   └── quality_predictor.py
│   │   ├── ml/
│   │   │   ├── train/
│   │   │   ├── inference/
│   │   │   └── artifacts/
│   │   ├── db/
│   │   │   ├── session.py
│   │   │   ├── base.py
│   │   │   └── seed.py
│   │   └── workers/
│   │       └── celery_app.py
│   └── tests/
│       ├── unit/
│       ├── integration/
│       └── e2e/
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   ├── index.html
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── router.tsx
│       ├── theme/
│       ├── components/
│       │   ├── common/
│       │   ├── charts/
│       │   ├── dashboard/
│       │   ├── presses/
│       │   ├── quality/
│       │   └── predictions/
│       ├── pages/
│       │   ├── Login.tsx
│       │   ├── Dashboard.tsx
│       │   ├── PressMonitor.tsx
│       │   ├── CureOptimizer.tsx
│       │   ├── QualityPrediction.tsx
│       │   ├── MoldAnomaly.tsx
│       │   ├── CompoundQuality.tsx
│       │   └── Reports.tsx
│       ├── api/
│       ├── hooks/
│       ├── store/
│       └── types/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── synthetic/
│   └── schemas/
├── infra/
│   ├── terraform/
│   ├── k8s/
│   └── nginx/
└── scripts/
    ├── init_db.sh
    ├── load_synthetic_data.py
    └── train_models.py
```

## ۲.۲ پشته فناوری

| لایه | فناوری |
|------|--------|
| Frontend | React 18 + TypeScript + Vite + MUI + Recharts + TanStack Query |
| Backend | Python 3.11 + FastAPI + SQLAlchemy 2 + Pydantic v2 |
| ML/AI | scikit-learn, PyTorch, XGBoost, SciPy (heat transfer), NumPy |
| پایگاه داده | PostgreSQL 16 + TimescaleDB (سری‌های زمانی) + Redis (cache) |
| صف کار | Celery + Redis |
| DevOps | Docker, Docker Compose, GitHub Actions, Prometheus + Grafana |
| احراز هویت | JWT + OAuth2 + RBAC |

---

<a name="3"></a>
# ۳. BRS – سند نیازمندی‌های کسب‌وکار

## ۳.۱ چشم‌انداز
تبدیل چرخه پخت ثابت به **چرخه پخت تطبیقی و پیش‌بینی کیفیت** بر اساس وضعیت واقعی هر پرس، برای ارتقای کیفیت، افزایش ظرفیت و کاهش مصرف انرژی در یزد تایر.

## ۳.۲ اهداف کسب‌وکار (KPIs)

| # | هدف | شاخص | مقدار هدف |
|---|------|------|-----------|
| B1 | کاهش زمان چرخه پخت | % کاهش میانگین زمان | ۵–۱۰٪ |
| B2 | کاهش مصرف بخار/انرژی | % کاهش مصرف | ۳–۸٪ |
| B3 | کاهش پخت ناکافی/بیش از حد | % کاهش ضایعات | ۲۰–۳۰٪ |
| B4 | ارتقای یکنواختی کیفیت | کاهش انحراف معیار آزمون یکنواختی | ۱۵٪ |
| B5 | تشخیص زودهنگام انحراف پرس/قالب | کاهش تایر معیوب کشف‌شده در بازار | ۴۰٪ |
| B6 | تأمین بودجه از اعتبار مالیاتی | % پوشش هزینه از اعتبار | ۱۰۰٪ هزینه مصوب |

## ۳.۳ ذی‌نفعان
- مدیرعامل و مدیران یزد تایر
- مدیران تولید و بهره‌برداران پرس‌ها
- کارشناسان کنترل کیفیت و آزمایشگاه
- واحد نگهداری و تعمیرات (قالب‌ها)
- واحد مالی (اعتبار مالیاتی)

## ۳.۴ دامنه (Scope)
**در دامنه:** چهار ماژول تخمین پخت، بهینه‌سازی چرخه/انرژی، پیش‌بینی کیفیت و تشخیص انحراف، پایش آمیزه؛ یکپارچه‌سازی داده پرس/بخار/آب داغ/نیتروژن؛ داشبورد مدیریتی.

**خارج از دامنه:** کنترل مستقیم PLC پرس‌ها (در فاز بعد)، تولید تایر، لجستیک.

## ۳.۵ مسیر تأمین بودجه
1. تدوین طرح نظام‌مند، نوآورانه و فناورانه با خروجی مشخص (محصول/بهبود فرآیند).
2. ثبت درخواست در `www.etebar.ir`.
3. تأیید توسط معاونت علمی و فناوری ریاست جمهوری.
4. کسر معادل کل هزینه‌های مصوب از مالیات عملکرد (قابل انتقال به سال‌های آینده).

**سرفصل هزینه‌های قابل پذیرش:** ۱) خرید ماشین‌آلات و تجهیزات ۲) هزینه نیروی انسانی ۳) خرید مواد اولیه، اجزا و قطعات ۴) هزینه آزمون‌ها و تست‌ها.

---

<a name="4"></a>
# ۴. SRS – سند نیازمندی‌های نرم‌افزار

## ۴.۱ نیازمندی‌های عملکردی (FR)

### ماژول ۱ – تخمین برخط میزان پخت (FR-1)
| کد | نیازمندی | اولویت |
|----|----------|--------|
| FR-1.1 | دریافت و یکپارچه‌سازی داده دما/فشار/زمان پرس، بخار، آب داغ، نیتروژن | باید |
| FR-1.2 | دریافت مشخصات و تاریخچه آمیزه، ابعاد و ساختار تایر | باید |
| FR-1.3 | محاسبه دمای نقاط بحرانی تایر با مدل انتقال حرارت + سینتیک پخت | باید |
| FR-1.4 | تخمین میزان پخت (Cure Degree) در طول چرخه به‌صورت برخط | باید |
| FR-1.5 | کالیبراسیون مدل با نتایج آزمون کیفی نمونه‌ها | باید |

### ماژول ۲ – بهینه‌سازی چرخه پخت و انرژی (FR-2)
| کد | نیازمندی | اولویت |
|----|----------|--------|
| FR-2.1 | محاسبه زمان چرخه بهینه تطبیقی برای هر محصول/آمیزه | باید |
| FR-2.2 | پیش‌بینی اثر تغییر بر ظرفیت، مصرف بخار و کیفیت | باید |
| FR-2.3 | پایش مستمر مصرف انرژی و ارائه تنظیمات پیشنهادی | باید |

### ماژول ۳ – پیش‌بینی کیفیت و تشخیص انحراف (FR-3)
| کد | نیازمندی | اولویت |
|----|----------|--------|
| FR-3.1 | پیش‌بینی احتمال معیوب بودن تایر پیش از خروج از پرس | باید |
| FR-3.2 | تشخیص انحراف تدریجی پرس/قالب (نشتی بخار، افت دما، گیر شیر) | باید |
| FR-3.3 | اعلام علت محتمل و اقدام پیشنهادی نگهداری | باید |

### ماژول ۴ – پایش کیفیت آمیزه (FR-4)
| کد | نیازمندی | اولویت |
|----|----------|--------|
| FR-4.1 | پایش فرآیند اختلاط و پیش‌بینی کیفیت آمیزه | باید |
| FR-4.2 | ایجاد زیرساخت دوقلوی دیجیتال فرآیند پخت | باید |

### نیازمندی‌های عمومی
| کد | نیازمندی |
|----|----------|
| FR-5.1 | داشبورد مدیریتی با KPIهای B1–B6 |
| FR-5.2 | مدیریت کاربران و RBAC |
| FR-5.3 | گزارش‌گیری و خروجی PDF/Excel |
| FR-5.4 | ثبت رویداد و Audit Log |
| FR-5.5 | API مبتنی بر OpenAPI برای یکپارچه‌سازی |

## ۴.۲ نیازمندی‌های غیرعملکردی (NFR)
| کد | نیازمندی | مقدار |
|----|----------|-------|
| NFR-1 | تأخیر تخمین برخط | < ۲ ثانیه |
| NFR-2 | دقت تخمین پخت | MAPE < ۵٪ |
| NFR-3 | دقت پیش‌بینی کیفیت | AUC ≥ ۰.۹ |
| NFR-4 | دسترس‌پذیری | ۹۹.۵٪ |
| NFR-5 | امنیت | OWASP Top 10، رمزنگاری TLS |
| NFR-6 | مقیاس‌پذیری | ≥ ۵۰ پرس همزمان |

## ۴.۳ نمودارهای محصول (درج در SRS)

### 4.3.1 نمودار زمینه (Context Diagram)
```
┌──────────────────────────────────────────────────────────────┐
│                    سامانه TCOP (یزد تایر)                    │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ ماژول ۱  │  │ ماژول ۲  │  │ ماژول ۳  │  │ ماژول ۴  │     │
│  │ تخمین    │  │ بهینه-   │  │ پیش-     │  │ پایش     │     │
│  │ پخت      │  │ سازی     │  │ بینی     │  │ آمیزه    │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘     │
│       └─────────────┴─────────────┴─────────────┘            │
│                          │                                   │
└──────────────────────────┼───────────────────────────────────┘
        │                 │                 │
   ┌────▼────┐      ┌─────▼─────┐     ┌────▼────┐
   │ پرس‌ها  │      │آزمایشگاه  │     │مدیریت   │
   │PLC/SCADA│      │کیفیت      │     │نگهداری  │
   └─────────┘      └───────────┘     └─────────┘
```

### 4.3.2 نمودار Use Case
```
        ┌─────────────────────────────────────────┐
        │              TCOP System                │
        │  ┌───────────────────────────────────┐  │
        │  │ (UC1) مشاهده تخمین برخط پخت      │  │
        │  │ (UC2) دریافت پیشنهاد زمان بهینه   │  │
        │  │ (UC3) مشاهده پیش‌بینی کیفیت       │  │
        │  │ (UC4) دریافت هشدار انحراف پرس     │  │
        │  │ (UC5) پایش کیفیت آمیزه            │  │
        │  │ (UC6) گزارش‌گیری مدیریتی           │  │
        │  │ (UC7) مدیریت کاربران              │  │
        │  └───────────────────────────────────┘  │
        └─────────────────────────────────────────┘
             ▲          ▲          ▲          ▲
             │          │          │          │
        ┌────┴───┐ ┌────┴───┐ ┌────┴───┐ ┌────┴───┐
        │بهره-   │ │کارشناس│ │مدیر    │ │مدیر    │
        │بردار   │ │کیفیت   │ │تولید   │ │سیستم   │
        └────────┘ └────────┘ └────────┘ └────────┘
```

### 4.3.3 نمودار ER (موجودیت–رابطه)
```
┌──────────┐     ┌───────────┐     ┌──────────┐
│  Press   │1───*│ CureCycle │*───1│   Tire   │
│ id (PK)  │     │ id (PK)   │     │ id (PK)  │
│ name     │     │ press_id  │     │ code     │
│ status   │     │ tire_id   │     │ compound │
└────┬─────┘     │ mold_id   │     │ structure│
     │           │ start/end │     └────┬─────┘
     │           │ temp/press│          │
     │           │ energy    │          │
     │           └─────┬─────┘          │
     │                 │                │
┌────▼─────┐     ┌─────▼──────┐   ┌─────▼──────┐
│   Mold   │1───*│ Prediction │*─1│QualityTest │
│ id (PK)  │     │ id (PK)    │   │ id (PK)    │
│ code     │     │ cure_cycle │   │ tire_id    │
│ status   │     │ cure_deg   │   │ uniformity │
│ cycles   │     │ quality_p  │   │ result     │
└──────────┘     │ anomaly_s  │   └────────────┘
                 └────────────┘
┌──────────┐     ┌───────────┐
│ Compound │1───*│  MixBatch │
│ id (PK)  │     │ id (PK)   │
│ code     │     │ compound  │
│ spec     │     │ mix_time  │
└──────────┘     │ quality   │
                 └───────────┘
```

### 4.3.4 نمودار توالی (Sequence) – چرخه پخت
```
کاربر       Frontend      API Gateway    Service        DB        ML Engine
 │             │              │            │            │            │
 │─درخواست────>│              │            │            │            │
 │             │─GET /cycle──>│            │            │            │
 │             │              │─validate──>│            │            │
 │             │              │            │─query─────>│            │
 │             │              │            │<─data──────│            │
 │             │              │            │─predict───────────────>│
 │             │              │            │<─cure_deg/quality──────│
 │             │              │<─response──│            │            │
 │<─نمایش──────│              │            │            │            │
```

### 4.3.5 نمودار مؤلفه (Component)
```
┌────────────┐   ┌────────────┐   ┌────────────┐
│ React SPA  │──>│ API Gateway│──>│ FastAPI    │
└────────────┘   └─────┬──────┘   │ Services   │
                       │          └─────┬──────┘
              ┌────────┴────────┐       │
              │ Auth (JWT/RBAC) │       │
              └─────────────────┘       │
        ┌───────────────┬───────────────┼───────────────┐
   ┌────▼────┐    ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
   │PostgreSQL│   │TimescaleDB│   │  Redis    │   │ ML Engine │
   │ (OLTP)   │   │(TimeSeries)│   │ (Cache)   │   │(PyTorch)  │
   └──────────┘   └───────────┘   └───────────┘   └───────────┘
```

### 4.3.6 نمودار استقرار (Deployment)
```
┌───────────────────────────────────────────────┐
│              Kubernetes Cluster               │
│  ┌─────────┐ ┌─────────┐ ┌───────────────┐   │
│  │ frontend│ │ backend │ │ ml-inference  │   │
│  │ (2 rep) │ │ (3 rep) │ │ (2 rep)       │   │
│  └────┬────┘ └────┬────┘ └───────┬───────┘   │
│       └───────────┴──────────────┘           │
│                   │                          │
│  ┌────────────────▼──────────────────────┐   │
│  │   PostgreSQL (Primary + Replica)      │   │
│  │   TimescaleDB + Redis                 │   │
│  └───────────────────────────────────────┘   │
└───────────────────────────────────────────────┘
         ▲                          ▲
   ┌─────┴─────┐              ┌─────┴─────┐
   │ PLC/SCADA │              │  کاربران  │
   │ (OT)      │              │  (IT)     │
   └───────────┘              └───────────┘
```

### 4.3.7 نمودار جریان داده فرآیند پخت
```
[سنسورهای پرس] ──> [جمع‌آوری داده] ──> [پیش‌پردازش] ──> [مدل انتقال حرارت]
                                                              │
[مشخصات آمیزه] ──────────────────────────────────────────────┤
[ساختار تایر] ───────────────────────────────────────────────┤
                                                              ▼
                                              [تخمین دمای نقاط بحرانی]
                                                              │
                                                              ▼
                                              [سینتیک پخت + ML] ──> [Cure Degree]
                                                              │
                                                              ▼
                                              [پیش‌بینی کیفیت + هشدار انحراف]
                                                              │
                                                              ▼
                                              [داشبورد + API + گزارش]
```

### 4.3.8 نمودار KPI (نمونه داشبورد)
```
┌──────────────────────────────────────────────────────────┐
│  داشبورد مدیریتی TCOP – یزد تایر                         │
├──────────────┬──────────────┬──────────────┬─────────────┤
│ زمان چرخه    │ مصرف بخار    │ ضایعات       │ یکنواختی    │
│ ▼ ۸.۲٪       │ ▼ ۶.۱٪       │ ▼ ۲۴٪        │ ▲ ۱۵٪       │
│ ▁▂▃▄▅▆▇      │ ▇▆▅▄▃▂▁      │ ▇▆▅▄▃▂▁      │ ▁▂▃▄▅▆▇     │
├──────────────┴──────────────┴──────────────┴─────────────┤
│  وضعیت پرس‌ها: ۱۲ سالم | ۲ هشدار | ۱ انحراف              │
│  پیش‌بینی کیفیت امروز: ۹۶.۴٪ سالم                        │
└──────────────────────────────────────────────────────────┘
```

---

<a name="5"></a>
# ۵. معماری Full-Stack

## ۵.۱ نمای کلی لایه‌ها
```
┌─────────────────────────────────────────────────────────┐
│ Presentation: React + TS + MUI + Recharts               │
├─────────────────────────────────────────────────────────┤
│ API Gateway: FastAPI + JWT + Rate Limit                 │
├─────────────────────────────────────────────────────────┤
│ Business Services: 4 ماژول + Optimizer + Anomaly        │
├─────────────────────────────────────────────────────────┤
│ ML Layer: Heat Transfer + Cure Kinetics + XGBoost/PyTorch│
├─────────────────────────────────────────────────────────┤
│ Data Layer: PostgreSQL + TimescaleDB + Redis            │
├─────────────────────────────────────────────────────────┤
│ Integration: OPC-UA / Modbus به PLC/SCADA               │
└─────────────────────────────────────────────────────────┘
```

## ۵.۲ نمونه کد Backend (FastAPI – سرویس بهینه‌سازی)

```python
# backend/app/services/optimizer.py
from dataclasses import dataclass
from typing import List
import numpy as np

@dataclass
class CureCycleInput:
    press_id: int
    tire_id: int
    compound_code: str
    target_cure_degree: float = 0.90
    current_temp_profile: List[float] = None
    steam_pressure: float = 0.0
    hot_water_temp: float = 0.0
    nitrogen_pressure: float = 0.0

class CureOptimizer:
    """ماژول ۲ – بهینه‌سازی تطبیقی زمان چرخه پخت"""

    def __init__(self, heat_model, kinetics_model, ml_model):
        self.heat = heat_model
        self.kinetics = kinetics_model
        self.ml = ml_model

    def optimize(self, inp: CureCycleInput) -> dict:
        # 1) شبیه‌سازی پروفایل دما در نقاط بحرانی
        temp_profile = self.heat.simulate(
            compound=inp.compound_code,
            steam_p=inp.steam_pressure,
            water_t=inp.hot_water_temp,
        )
        # 2) محاسبه درجه پخت
        cure_deg = self.kinetics.integrate(temp_profile)
        # 3) یافتن کمینه زمان با حفظ حاشیه کیفی
        t_opt = self._find_min_time(cure_deg, inp.target_cure_degree)
        # 4) پیش‌بینی کیفیت و انرژی با ML
        quality = self.ml.predict_quality(inp, t_opt)
        energy = self.ml.predict_energy(inp, t_opt)
        return {
            "optimal_time_min": round(t_opt, 2),
            "predicted_cure_degree": round(float(cure_deg[-1]), 3),
            "predicted_quality_prob": round(float(quality), 3),
            "predicted_energy_kwh": round(float(energy), 2),
            "savings_vs_baseline_pct": self._savings(t_opt),
        }

    def _find_min_time(self, cure_deg, target):
        idx = np.where(cure_deg >= target)[0]
        return idx[0] if len(idx) else len(cure_deg)

    def _savings(self, t_opt):
        baseline = 22.0  # دقیقه – نمونه
        return round((baseline - t_opt) / baseline * 100, 2)
```

## ۵.۳ نمونه کد Frontend (React – داشبورد)

```tsx
// frontend/src/pages/Dashboard.tsx
import { useQuery } from "@tanstack/react-query";
import { Grid, Card, CardContent, Typography } from "@mui/material";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { fetchKpis } from "../api/kpi";

export default function Dashboard() {
  const { data } = useQuery({ queryKey: ["kpis"], queryFn: fetchKpis });

  return (
    <Grid container spacing={2} p={2}>
      {data?.kpis.map((k) => (
        <Grid item xs={12} md={3} key={k.id}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2">{k.title}</Typography>
              <Typography variant="h4">{k.value}</Typography>
              <Typography color={k.trend > 0 ? "success.main" : "error.main"}>
                {k.trend > 0 ? "▲" : "▼"} {Math.abs(k.trend)}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h6">روند زمان چرخه پخت</Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={data?.cycleTrend ?? []}>
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="minutes" stroke="#1976d2" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
}
```

---

<a name="6"></a>
# ۶. مدل داده و کدنویسی تمامی ردیف‌های داده

## ۶.۱ طرح جداول (TimescaleDB + PostgreSQL)

```sql
-- 1) پرس‌ها
CREATE TABLE presses (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(64) NOT NULL,
    model         VARCHAR(64),
    status        VARCHAR(16) DEFAULT 'active',
    installed_at  DATE,
    created_at    TIMESTAMPTZ DEFAULT now()
);

-- 2) آمیزه‌ها
CREATE TABLE compounds (
    id            SERIAL PRIMARY KEY,
    code          VARCHAR(32) UNIQUE NOT NULL,
    name          VARCHAR(128),
    spec_json     JSONB,          -- مشخصات فنی
    created_at    TIMESTAMPTZ DEFAULT now()
);

-- 3) تایرها
CREATE TABLE tires (
    id            SERIAL PRIMARY KEY,
    code          VARCHAR(64) UNIQUE NOT NULL,
    compound_id   INT REFERENCES compounds(id),
    structure_json JSONB,         -- ابعاد و ساختار
    created_at    TIMESTAMPTZ DEFAULT now()
);

-- 4) قالب‌ها
CREATE TABLE molds (
    id            SERIAL PRIMARY KEY,
    code          VARCHAR(64) UNIQUE NOT NULL,
    press_id      INT REFERENCES presses(id),
    status        VARCHAR(16) DEFAULT 'ok',
    total_cycles  INT DEFAULT 0,
    last_service  DATE
);

-- 5) چرخه‌های پخت (TimeSeries)
CREATE TABLE cure_cycles (
    id            BIGSERIAL,
    press_id      INT REFERENCES presses(id),
    tire_id       INT REFERENCES tires(id),
    mold_id       INT REFERENCES molds(id),
    start_ts      TIMESTAMPTZ NOT NULL,
    end_ts        TIMESTAMPTZ,
    duration_min  NUMERIC(6,2),
    steam_pressure NUMERIC(6,3),
    hot_water_temp NUMERIC(6,2),
    nitrogen_pressure NUMERIC(6,3),
    energy_kwh    NUMERIC(8,2),
    PRIMARY KEY (id, start_ts)
);
SELECT create_hypertable('cure_cycles', 'start_ts');

-- 6) سری زمانی سنسورها
CREATE TABLE sensor_readings (
    time          TIMESTAMPTZ NOT NULL,
    press_id      INT,
    sensor        VARCHAR(32),   -- temp, pressure, ...
    value         DOUBLE PRECISION
);
SELECT create_hypertable('sensor_readings', 'time');

-- 7) آزمون‌های کیفی
CREATE TABLE quality_tests (
    id            BIGSERIAL PRIMARY KEY,
    tire_id       INT REFERENCES tires(id),
    test_type     VARCHAR(32),   -- uniformity, ...
    result_json   JSONB,
    passed        BOOLEAN,
    tested_at     TIMESTAMPTZ DEFAULT now()
);

-- 8) پیش‌بینی‌ها
CREATE TABLE predictions (
    id            BIGSERIAL PRIMARY KEY,
    cure_cycle_id BIGINT,
    cure_degree   NUMERIC(5,4),
    quality_prob  NUMERIC(5,4),
    anomaly_score NUMERIC(5,4),
    model_version VARCHAR(32),
    created_at    TIMESTAMPTZ DEFAULT now()
);

-- 9) کاربران و نقش‌ها
CREATE TABLE users (
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(64) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role          VARCHAR(32) NOT NULL,
    is_active     BOOLEAN DEFAULT true
);
```

## ۶.۲ کدنویسی تمامی ردیف‌های داده (Seed / Synthetic Loader)

```python
# scripts/load_synthetic_data.py
"""تولید و درج تمامی ردیف‌های داده نمونه برای TCOP"""
import random, json
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

ENGINE = create_engine("postgresql://tcop:tcop@localhost:5432/tcop")
random.seed(42)

# ---------- 1) Presses ----------
presses = [{"name": f"Press-{i:02d}", "model": "YZ-2000", "installed_at": "2020-01-01"}
           for i in range(1, 16)]

# ---------- 2) Compounds ----------
compounds = [
    {"code": "CMP-A1", "name": "Tread Compound A1", "spec_json": {"density": 1.15, "k": 0.25}},
    {"code": "CMP-B2", "name": "Sidewall Compound B2", "spec_json": {"density": 1.10, "k": 0.22}},
    {"code": "CMP-C3", "name": "Inner Liner C3", "spec_json": {"density": 1.20, "k": 0.28}},
]

# ---------- 3) Tires ----------
tires = [{"code": f"TIRE-{i:04d}",
          "compound_code": random.choice(compounds)["code"],
          "structure_json": {"width": 205, "ratio": 55, "rim": 16, "layers": 4}}
         for i in range(1, 101)]

# ---------- 4) Molds ----------
molds = [{"code": f"MOLD-{i:03d}", "press_id": i % 15 + 1,
          "status": "ok", "total_cycles": random.randint(0, 5000),
          "last_service": "2024-06-01"} for i in range(1, 31)]

# ---------- 5) Cure Cycles + Sensors + Predictions ----------
cycles, sensors, preds = [], [], []
base = datetime(2025, 1, 1)
for i in range(1, 2001):
    press_id = random.randint(1, 15)
    tire_id  = random.randint(1, 100)
    mold_id  = random.randint(1, 30)
    start    = base + timedelta(minutes=i * 25)
    dur      = random.uniform(18.0, 26.0)
    end      = start + timedelta(minutes=dur)
    cycles.append({
        "press_id": press_id, "tire_id": tire_id, "mold_id": mold_id,
        "start_ts": start, "end_ts": end, "duration_min": round(dur, 2),
        "steam_pressure": round(random.uniform(1.2, 1.8), 3),
        "hot_water_temp": round(random.uniform(160, 180), 2),
        "nitrogen_pressure": round(random.uniform(1.0, 1.4), 3),
        "energy_kwh": round(random.uniform(40, 70), 2),
    })
    # sensors (نمونه 10 خوانش در هر چرخه)
    for t in range(10):
        sensors.append({"time": start + timedelta(minutes=t * dur / 10),
                        "press_id": press_id, "sensor": "temp",
                        "value": round(150 + random.uniform(-8, 8), 2)})
    # prediction
    preds.append({"cure_cycle_id": i,
                  "cure_degree": round(random.uniform(0.85, 1.0), 4),
                  "quality_prob": round(random.uniform(0.80, 0.99), 4),
                  "anomaly_score": round(random.uniform(0.0, 0.4), 4),
                  "model_version": "v1.0"})

# ---------- 6) Quality Tests ----------
qts = []
for tire_id in range(1, 101):
    for j in range(3):
        qts.append({"tire_id": tire_id, "test_type": "uniformity",
                    "result_json": json.dumps({"radial": random.uniform(0, 5),
                                                "lateral": random.uniform(0, 5)}),
                    "passed": random.random() > 0.15})

# ---------- Insert ----------
def insert(table, rows):
    if not rows:
        return
    cols = rows[0].keys()
    sql = text(f"INSERT INTO {table} ({','.join(cols)}) VALUES ({','.join(':'+c for c in cols)})")
    with ENGINE.begin() as conn:
        conn.execute(sql, rows)

insert("presses", presses)
insert("compounds", compounds)
insert("tires", tires)
insert("molds", molds)
insert("cure_cycles", cycles)
insert("sensor_readings", sensors)
insert("quality_tests", qts)
insert("predictions", preds)

print("✅ داده‌های نمونه با موفقیت درج شدند.")
```

## ۶.۳ نمونه کد ML (تخمین پخت + پیش‌بینی کیفیت)

```python
# backend/app/services/ml_models.py
import numpy as np
from scipy.integrate import solve_ivp
from sklearn.ensemble import GradientBoostingClassifier
import joblib, os

class HeatTransferModel:
    """مدل انتقال حرارت یک‌بعدی برای نقاط بحرانی تایر"""
    def __init__(self, alpha=1.2e-7, thickness=0.025):
        self.alpha = alpha      # ضریب نفوذ حرارتی (m^2/s)
        self.L = thickness

    def simulate(self, compound, steam_p, water_t, n=60, t_max=1500):
        T0 = 25.0
        Ts = water_t
        dx = self.L / n
        x = np.linspace(0, self.L, n)
        T = np.full(n, T0)

        def rhs(t, T):
            dT = np.zeros_like(T)
            for i in range(1, n-1):
                dT[i] = self.alpha * (T[i+1] - 2*T[i] + T[i-1]) / dx**2
            dT[0] = (Ts - T[0]) * 1e-3
            dT[-1] = 0
            return dT

        sol = solve_ivp(rhs, (0, t_max), T, t_eval=np.linspace(0, t_max, 300))
        return sol.y[-1]  # دمای مرکز در انتها

class CureKineticsModel:
    """سینتیک پخت با معادله آرنیوس"""
    def __init__(self, Ea=80000, k0=1e10, n=1.5):
        self.Ea, self.k0, self.n = Ea, k0, n
        self.R = 8.314

    def integrate(self, temp_profile, dt=1.0):
        cure = np.zeros(len(temp_profile))
        for i in range(1, len(temp_profile)):
            T = temp_profile[i] + 273.15
            k = self.k0 * np.exp(-self.Ea / (self.R * T))
            cure[i] = cure[i-1] + k * (1 - cure[i-1])**self.n * dt
            cure[i] = min(cure[i], 1.0)
        return cure

class QualityPredictor:
    """پیش‌بینی کیفیت با Gradient Boosting"""
    def __init__(self, model_path="artifacts/quality_gb.pkl"):
        self.model = joblib.load(model_path) if os.path.exists(model_path) else None

    def predict_quality(self, features: dict, t_opt: float) -> float:
        if self.model is None:
            return 0.95
        X = np.array([[features["steam_pressure"],
                       features["hot_water_temp"],
                       features["nitrogen_pressure"],
                       t_opt]])
        return float(self.model.predict_proba(X)[0][1])
```

---

<a name="7"></a>
# ۷. طراحی UI/UX

## ۷.۱ اصول طراحی
- **RTL کامل** و فونت فارسی (Vazirmatn)
- **رنگ سازمانی**: آبی صنعتی `#1976d2`، سبز موفقیت `#2e7d32`، نارنجی هشدار `#ed6c02`، قرمز خطا `#d32f2f`
- **دسترس‌پذیری**: WCAG 2.1 AA
- **طراحی واکنش‌گرا** برای دسکتاپ کارخانه و تبلت بهره‌بردار

## ۷.۲ ساختار صفحات
| صفحه | توضیح |
|------|-------|
| `Login` | ورود با JWT و RBAC |
| `Dashboard` | KPIهای B1–B6، وضعیت پرس‌ها، روندها |
| `PressMonitor` | مانیتور لحظه‌ای پرس‌ها + نمودار دما/فشار |
| `CureOptimizer` | ورودی شرایط، خروجی زمان بهینه + صرفه‌جویی |
| `QualityPrediction` | پیش‌بینی کیفیت هر تایر پیش از خروج |
| `MoldAnomaly` | هشدار انحراف قالب/پرس + علت محتمل |
| `CompoundQuality` | پایش آمیزه و اختلاط |
| `Reports` | خروجی PDF/Excel و گزارش‌های دوره‌ای |

## ۷.۳ ماکاپ متنی Dashboard
```
┌──────────────────────────────────────────────────────────────┐
│  🏭 TCOP – داشبورد مدیریتی          کاربر: مدیر تولید  ⚙️  │
├──────────────────────────────────────────────────────────────┤
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│ │زمان چرخه │ │مصرف بخار │ │ضایعات    │ │یکنواختی  │         │
│ │ ▼۸.۲٪    │ │ ▼۶.۱٪    │ │ ▼۲۴٪     │ │ ▲۱۵٪     │         │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘         │
├──────────────────────────────────────────────────────────────┤
│  وضعیت پرس‌ها:  🟢۱۲ سالم  🟠۲ هشدار  🔴۱ انحراف            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  نمودار روند زمان چرخه پخت (Recharts LineChart)      │   │
│  │  ▁▂▃▄▅▆▇█  (۳۰ روز اخیر)                            │   │
│  └──────────────────────────────────────────────────────┘   │
├──────────────────────────────────────────────────────────────┤
│  پیش‌بینی کیفیت امروز: ۹۶.۴٪ سالم                            │
│  هشدارها: [MOLD-014 انحراف دما] [Press-07 نشتی بخار]        │
└──────────────────────────────────────────────────────────────┘
```

## ۷.۴ رنگ‌بندی وضعیت
| وضعیت | رنگ | کد |
|-------|-----|-----|
| سالم | سبز | `#2e7d32` |
| هشدار | نارنجی | `#ed6c02` |
| انحراف | قرمز | `#d32f2f` |
| اطلاعات | آبی | `#1976d2` |

---

<a name="8"></a>
# ۸. README – راهنمای پروژه

```markdown
# TCOP – سامانه هوشمند بهینه‌سازی چرخه پخت و پیش‌بینی کیفیت تایر

سامانه‌ای مبتنی بر هوش مصنوعی برای **شرکت یزد تایر** که چرخه پخت ثابت را به
**چرخه تطبیقی و پیش‌بینی کیفیت** تبدیل می‌کند.

## ✨ ویژگی‌ها
- تخمین برخط میزان پخت در نقاط بحرانی تایر
- بهینه‌سازی تطبیقی زمان چرخه و مصرف انرژی
- پیش‌بینی کیفیت تایر و تشخیص انحراف پرس/قالب
- پایش کیفیت آمیزه و فرآیند اختلاط
- داشبورد مدیریتی با KPIهای کسب‌وکار

## 🚀 اجرا (Docker)

```bash
cp .env.example .env
docker compose up --build -d
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

## 🧪 تست

```bash
cd backend && pytest -q
cd frontend && npm test
```

## 📊 داده نمونه

```bash
python scripts/load_synthetic_data.py
python scripts/train_models.py
```

## 🏗️ ساختار
- `backend/` – FastAPI + SQLAlchemy + ML
- `frontend/` – React + TS + MUI + Recharts
- `docs/` – BRS، SRS، معماری، نمودارها
- `data/` – داده خام، پردازش‌شده، سنتتیک
- `infra/` – Terraform، K8s، Nginx

## 💰 تأمین بودجه
مطابق بند «ب» ماده ۱۱ قانون جهش تولید دانش‌بنیان (۱۴۰۱)، هزینه‌های تحقیق
و توسعه این طرح پس از تأیید معاونت علمی و فناوری ریاست جمهوری از طریق
سامانه [www.etebar.ir](https://www.etebar.ir) قابل کسر از مالیات عملکرد است.

## 📄 مجوز
Internal – PetroPalatus Co. © 2025
```

---

<a name="9"></a>
# ۹. نقشه راه بلوغ ۴ (Maturity Level 4)

| مرحله | خروجی | معیار پذیرش |
|-------|-------|-------------|
| M1 – Concept | BRS، SRS، معماری | تأیید ذی‌نفعان |
| M2 – Prototype | Mockup UI، API stub، مدل حرارتی | اجرای end-to-end نمونه |
| M3 – Integrated | ۴ ماژول یکپارچه + داده سنتتیک | دقت MAPE < ۵٪ روی داده سنتتیک |
| **M4 – Lab Validation** | اعتبارسنجی با داده واقعی آزمایشگاه یزد تایر | AUC ≥ ۰.۹، تأخیر < ۲s، تأییدیه کیفیت |
| M5 – Pilot (آینده) | پایلوت صنعتی روی ۵ پرس | KPIهای B1–B6 محقق شود |

## معیارهای پذیرش سطح ۴
1. **اعتبارسنجی مدل انتقال حرارت** با حداقل ۳۰ چرخه واقعی آزمایشگاه.
2. **دقت پیش‌بینی کیفیت** AUC ≥ ۰.۹ روی مجموعه آزمون.
3. **تأخیر تخمین برخط** < ۲ ثانیه در ۵۰ درخواست همزمان.
4. **پوشش تست** ≥ ۸۰٪ برای سرویس‌های حیاتی.
5. **مستندسازی کامل** SRS، BRS، API و نمودارها.
6. **آمادگی مالی:** تدوین مستندات اعتبار مالیاتی جهت ثبت در `etebar.ir`.

---

## ✅ جمع‌بندی تحویل‌دادنی‌ها

| # | تحویل‌دادنی | وضعیت |
|---|-------------|--------|
| 1 | اسکفلد پروژه کامل | ✅ |
| 2 | BRS | ✅ |
| 3 | SRS + ۸ نمودار | ✅ |
| 4 | معماری Full-Stack | ✅ |
| 5 | کدنویسی تمامی ردیف‌های داده (۹ جدول + Seed) | ✅ |
| 6 | طراحی UI/UX | ✅ |
| 7 | README | ✅ |
| 8 | نقشه راه بلوغ ۴ | ✅ |

---

> **تهیه‌کننده:** تیم فنی پتروپالاتوس – مطابق نامه شماره ۱۴۰۵۰۹۰۲۰۰۱ خطاب به جناب آقای مهندس احمد رضوانی، مدیرعامل شرکت یزد تایر.
>
> **مسیر بودجه:** `www.etebar.ir` – اعتبار مالیاتی تحقیق و توسعه (بند ب ماده ۱۱ قانون جهش تولید دانش‌بنیان).

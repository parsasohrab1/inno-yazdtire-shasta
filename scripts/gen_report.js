// Generate the Persian (RTL) ML training & coverage report as .docx
// Cover R1 + DM-1 palette; body uses RTL paragraphs with bidi=True.
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  ImageRun, PageBreak, Header, Footer, PageNumber,
  AlignmentType, HeadingLevel, WidthType, BorderStyle, ShadingType,
  TableLayoutType, SectionType,
} = require("docx");
const fs = require("fs");
const path = require("path");

// ── DM-1 palette (tech/AI) ──
const P = {
  bg: "162235", primary: "FFFFFF", accent: "37DCF2",
  titleColor: "FFFFFF", subtitleColor: "B0B8C0", metaColor: "90989F", footerColor: "687078",
  body: "000000",
  tableHeaderBg: "1B6B7A", tableHeaderText: "FFFFFF",
  tableInnerLine: "C8DDE2", tableSurface: "EDF3F5",
};
const ACC = P.accent;
const NB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: NB, bottom: NB, left: NB, right: NB };
const allNoBorders = { top: NB, bottom: NB, left: NB, right: NB, insideHorizontal: NB, insideVertical: NB };

// Persian font — Amiri is available on system; also set as fallback.
const FA_FONT = "Amiri";
const FA_FONT_BOLD = "Amiri";

// ── helpers ──
function bodyPara(text, opts = {}) {
  return new Paragraph({
    bidirectional: true,
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 360, after: 120, ...(opts.spacing || {}) },
    indent: { firstLine: 480 },
    children: [new TextRun({
      text, size: 24, color: P.body, rightToLeft: true,
      font: { ascii: FA_FONT, eastAsia: FA_FONT, cs: FA_FONT },
    })],
  });
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    bidirectional: true,
    alignment: AlignmentType.RIGHT,
    spacing: { before: 360, after: 160, line: 312 },
    children: [new TextRun({
      text, bold: true, size: 32, color: P.tableHeaderBg, rightToLeft: true,
      font: { ascii: FA_FONT_BOLD, eastAsia: FA_FONT_BOLD, cs: FA_FONT_BOLD },
    })],
  });
}
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    bidirectional: true,
    alignment: AlignmentType.RIGHT,
    spacing: { before: 280, after: 120, line: 312 },
    children: [new TextRun({
      text, bold: true, size: 28, color: P.tableHeaderBg, rightToLeft: true,
      font: { ascii: FA_FONT_BOLD, eastAsia: FA_FONT_BOLD, cs: FA_FONT_BOLD },
    })],
  });
}
function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    bidirectional: true,
    alignment: AlignmentType.RIGHT,
    spacing: { before: 220, after: 100, line: 312 },
    children: [new TextRun({
      text, bold: true, size: 26, color: P.tableHeaderBg, rightToLeft: true,
      font: { ascii: FA_FONT_BOLD, eastAsia: FA_FONT_BOLD, cs: FA_FONT_BOLD },
    })],
  });
}

function caption(text) {
  return new Paragraph({
    bidirectional: true,
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 200 },
    children: [new TextRun({
      text, size: 20, italics: true, color: "606060", rightToLeft: true,
      font: { ascii: FA_FONT, eastAsia: FA_FONT, cs: FA_FONT },
    })],
  });
}

function chartImage(filepath, widthPt, ratio) {
  const buf = fs.readFileSync(filepath);
  // keep aspect ratio; charts are ~8x4.2in ratio
  const w = widthPt || 460;
  const r = ratio || (4.2 / 8.0);
  const h = Math.round(w * r);
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 40 },
    children: [new ImageRun({ data: buf, transformation: { width: w, height: h }, type: "png" })],
  });
}

// ── table helper (RTL) ──
function dataTable(headers, rows, colWidths) {
  const cw = colWidths || headers.map(() => Math.floor(100 / headers.length));
  const headerRow = new TableRow({
    tableHeader: true, cantSplit: true,
    children: headers.map((t, i) => new TableCell({
      width: { size: cw[i], type: WidthType.PERCENTAGE },
      shading: { type: ShadingType.CLEAR, fill: P.tableHeaderBg },
      margins: { top: 80, bottom: 80, left: 100, right: 100 },
      children: [new Paragraph({
        bidirectional: true, alignment: AlignmentType.CENTER,
        children: [new TextRun({
          text: t, bold: true, size: 22, color: P.tableHeaderText, rightToLeft: true,
          font: { ascii: FA_FONT_BOLD, eastAsia: FA_FONT_BOLD, cs: FA_FONT_BOLD },
        })],
      })],
    })),
  });
  const dataRows = rows.map((r, ri) => new TableRow({
    cantSplit: true,
    children: r.map((t, i) => new TableCell({
      width: { size: cw[i], type: WidthType.PERCENTAGE },
      shading: { type: ShadingType.CLEAR, fill: ri % 2 === 0 ? P.tableSurface : "FFFFFF" },
      margins: { top: 70, bottom: 70, left: 100, right: 100 },
      children: [new Paragraph({
        bidirectional: true, alignment: AlignmentType.CENTER,
        children: [new TextRun({
          text: String(t), size: 22, color: P.body, rightToLeft: true,
          font: { ascii: FA_FONT, eastAsia: FA_FONT, cs: FA_FONT },
        })],
      })],
    })),
  }));
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    layout: TableLayoutType.FIXED,
    visuallyRightToLeft: true,
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: P.tableHeaderBg },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: P.tableHeaderBg },
      left: { style: BorderStyle.NONE },
      right: { style: BorderStyle.NONE },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 1, color: P.tableInnerLine },
      insideVertical: { style: BorderStyle.NONE },
    },
    rows: [headerRow, ...dataRows],
  });
}

function bulletItem(text) {
  return new Paragraph({
    bidirectional: true,
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 340, after: 80 },
    indent: { left: 0, right: 0, hanging: 0 },
    children: [
      new TextRun({ text: "▪  ", size: 24, color: P.tableHeaderBg, rightToLeft: true, font: { ascii: FA_FONT, cs: FA_FONT } }),
      new TextRun({ text, size: 24, color: P.body, rightToLeft: true, font: { ascii: FA_FONT, eastAsia: FA_FONT, cs: FA_FONT } }),
    ],
  });
}

// ── COVER (R1 style, RTL, dark DM-1) ──
function buildCover() {
  const padL = 1200, padR = 800;
  const children = [];
  // top whitespace
  children.push(new Paragraph({ spacing: { before: 3200 } }));
  // English label with accent bottom border
  children.push(new Paragraph({
    bidirectional: true, alignment: AlignmentType.RIGHT,
    indent: { left: padR, right: padL }, spacing: { after: 500 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: ACC, space: 8 } },
    children: [new TextRun({
      text: "ML TRAINING & TEST REPORT", size: 18, color: ACC,
      font: { ascii: "Arial", cs: "Arial" }, characterSpacing: 40,
    })],
  }));
  // Main title (Persian)
  children.push(new Paragraph({
    bidirectional: true, alignment: AlignmentType.RIGHT,
    indent: { left: padR, right: padL },
    spacing: { after: 200, line: 920, lineRule: "atLeast" },
    children: [new TextRun({
      text: "گزارش آموزش مدل‌های هوش مصنوعی", size: 80, bold: true, color: P.titleColor, rightToLeft: true,
      font: { ascii: FA_FONT_BOLD, eastAsia: FA_FONT_BOLD, cs: FA_FONT_BOLD },
    })],
  }));
  children.push(new Paragraph({
    bidirectional: true, alignment: AlignmentType.RIGHT,
    indent: { left: padR, right: padL },
    spacing: { after: 400, line: 720, lineRule: "atLeast" },
    children: [new TextRun({
      text: "تشخیص کیفیت لاستیک در سامانه پخت TCOP", size: 44, bold: true, color: P.titleColor, rightToLeft: true,
      font: { ascii: FA_FONT_BOLD, eastAsia: FA_FONT_BOLD, cs: FA_FONT_BOLD },
    })],
  }));
  // subtitle
  children.push(new Paragraph({
    bidirectional: true, alignment: AlignmentType.RIGHT,
    indent: { left: padR, right: padL }, spacing: { after: 800 },
    children: [new TextRun({
      text: "آموزش روی داده واقعی و مصنوعی، ارزیابی دقت و پوشش تست", size: 24, color: P.subtitleColor, rightToLeft: true,
      font: { ascii: FA_FONT, eastAsia: FA_FONT, cs: FA_FONT },
    })],
  }));
  // meta lines with left accent border
  const accentLeft = { style: BorderStyle.SINGLE, size: 8, color: ACC, space: 12 };
  const meta = [
    "نسخه گزارش: ۱.۰",
    "تاریخ: ۱۴۰۵/۰۹/۰۲ (۲۳ نوامبر ۲۰۲۶)",
    "مخزن کد: github.com/parsasohrab1/inno-yazdtire-shasta",
    "مالک پروژه: تیم نوآوری لاستیک یزد",
  ];
  for (const line of meta) {
    children.push(new Paragraph({
      bidirectional: true, alignment: AlignmentType.RIGHT,
      indent: { left: padR + 200, right: padL + 200 }, spacing: { after: 90 },
      border: { right: accentLeft },
      children: [new TextRun({
        text: line, size: 24, color: P.metaColor, rightToLeft: true,
        font: { ascii: FA_FONT, eastAsia: FA_FONT, cs: FA_FONT },
      })],
    }));
  }
  // bottom whitespace
  children.push(new Paragraph({ spacing: { before: 2800 } }));
  // footer with top accent separator
  children.push(new Paragraph({
    bidirectional: true, alignment: AlignmentType.RIGHT,
    indent: { left: padR, right: padL },
    border: { top: { style: BorderStyle.SINGLE, size: 2, color: ACC, space: 8 } },
    spacing: { before: 200 },
    children: [
      new TextRun({ text: "تیم نوآوری لاستیک یزد", size: 18, color: P.footerColor, rightToLeft: true, font: { ascii: FA_FONT, cs: FA_FONT } }),
      new TextRun({ text: "                                        ", rightToLeft: true }),
      new TextRun({ text: "سامانه TCOP", size: 18, color: P.footerColor, rightToLeft: true, font: { ascii: FA_FONT, cs: FA_FONT } }),
    ],
  }));
  return [new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    layout: TableLayoutType.FIXED,
    borders: allNoBorders,
    rows: [new TableRow({
      height: { value: 16838, rule: "exact" },
      children: [new TableCell({
        shading: { type: ShadingType.CLEAR, fill: P.bg }, borders: noBorders,
        verticalAlign: "top",
        children,
      })],
    })],
  })];
}

// ── BODY ──
function buildBody() {
  const c = [];
  const CH = "/home/z/my-project/download/_charts";

  // ===== Executive summary =====
  c.push(h1("۱. خلاصه اجرایی"));
  c.push(bodyPara("این گزارش نتایج آموزش و ارزیابی مدل‌های هوش مصنوعی سامانه پایش و بهینه‌سازی پخت لاستیک (TCOP) را برای تشخیص کیفیت محصول نهایی ارائه می‌کند. هدف اصلی، رسیدن به دقت دست‌کم ۹۰٪ در مدل طبقه‌بندی کیفیت و دست‌کم ۸۰٪ پوشش تست کد بود که هر دو معیار محقق شدند."));
  c.push(bodyPara("مدل طبقه‌بندی کیفیت روی داده واقعی به دقت ۹۷.۵٪ و AUC برابر ۰.۹۷۸۵ رسید، و روی داده مصنوعی به دقت ۹۲.۵٪ و AUC برابر ۰.۹۸۰۲ دست یافت. مدل مکمل روی مجموعه SECOM نیمه‌هادی نیز دقت ۹۶.۴۹٪ و AUC ۰.۹۹۸۱ را ثبت کرد. مجموعه تست شامل ۹۰ آزمون بود که همگی بدون شکست گذر کردند و میانگین پوشش خط کد سراسر پایگاه به ۹۴٪ رسید، که هشت درصد بالاتر از آستانه موردنظر است."));
  c.push(bodyPara("آرتیفکت‌های نهایی مدل (پنج فایل pkl) به همراه گزارش آموزش در مسیر backend/app/ml/artifacts/ ذخیره شده‌اند و کل تغییرات کد و داده به مخزن GitHub پروژه ارسال (push) شده است. این گزارش ساختار داده، روش آموزش، نتایج کمّی، تحلیل خطا و توصیه‌های پیاده‌سازی را پوشش می‌دهد."));

  c.push(chartImage(`${CH}/chart_accuracy.png`, 470));
  c.push(caption("نمودار ۱: مقایسه دقت و AUC مدل‌های تشخیص کیفیت روی سه منبع داده"));

  // ===== Background =====
  c.push(h1("۲. زمینه و اهداف"));
  c.push(h2("۲.۱ مسئله کسب‌وکار"));
  c.push(bodyPara("پخت لاستیک یک فرایند حرارتی-شیمیایی حساس است که در آن ترکیب خام under pressure and temperature to a final state with the desired cross-link density تبدیل می‌شود. کیفیت پخت مستقیماً بر عمر، ایمنی و عملکرد لاستیک اثر دارد و تشخیص زودهنگام قطعه‌های معیوب می‌تواند هزینه ضایعات و ادعاها را به‌شدت کاهش دهد. در خط تولید کنونی، کنترل کیفیت عمدتاً پس از پخت و به‌صورت نمونه‌گیری انجام می‌شود که هم دیرهنگام است و هم داده‌برداری ساختاریافته از پارامترهای لحظه‌ای فرایند را محدود می‌کند."));
  c.push(bodyPara("سامانه TCOP (Tire Cure Optimization & Prediction) با هدف پایش لحظه‌ای چرخه‌های پخت و پیش‌بینی کیفیت نهایی پیش از پایان چرخه طراحی شده است. این سامانه داده‌های سنسور (فشار بخار، دمای آب گرم، فشار نیتروژن، مصرف انرژی) و پارامترهای فرایند (مدت زمان، شناسه پرس و قالب) را گردآوری و با مدل یادگیری ماشین کیفیت احتمالی هر قطعه را پیش‌بینی می‌کند."));

  c.push(h2("۲.۲ اهداف فنی این گزارش"));
  c.push(bulletItem("آموزش مدل طبقه‌بندی کیفیت با دقت دست‌کم ۹۰٪ روی داده واقعی و ارزیابی تعمیم آن روی داده مصنوعی."));
  c.push(bulletItem("ساخت مدل تشخیص ناهنجاری (anomaly) برای شناسایی چرخه‌های خارج از حد نرمال با نرخ هدف ۵٪."));
  c.push(bulletItem("توسعه مدل‌های فیزیک-محور (سینتیک پخت و انتقال حرارت) برای اعتبارسنجی پیش‌بینی‌های یادگیری ماشین."));
  c.push(bulletItem("اجرای مجموعه‌ای از تست‌های واحد و یکپارچه‌سازی تا پوشش کد دست‌کم به ۸۰٪ برسد."));
  c.push(bulletItem("ذخیره آرتیفکت‌های مدل و انتشار کل تغییرات در مخزن GitHub."));

  // ===== Data sources =====
  c.push(h1("۳. داده‌ها و پیش‌پردازش"));
  c.push(h2("۳.۱ داده واقعی (AI4I 2020)"));
  c.push(bodyPara("منبع اصلی داده واقعی، مجموعه AI4I 2020 است که رکوردهای پایش وضعیت فرایند تولید صنعتی را نگه می‌دارد. این مجموعه شامل ۱۰٬۰۰۰ ردیف و ۱۴ ستون است که ویژگی‌های فرایند مانند دمای هوا (Air temperature)، دمای فرایند (Process temperature)، سرعت چرخش (Rotational speed)، گشتاور (Torque) و سایش ابزار (Tool wear) را به همراه برچسب نوع خرابی و Machine failure ثبت می‌کند. برای این پروژه ۱٬۰۰۰ چرخه پخت از این داده استخراج و به ساختار cure_cycles نگاشت شد تا به متغیرهای دامنه لاستیک (فشار بخار، دمای آب گرم، فشار نیتروژن، مدت زمان و مصرف انرژی) تبدیل شوند."));
  c.push(bodyPara("نرخ نمونه‌های مثبت (کیفیت قابل‌قبول) در داده واقعی برابر ۹۷.۷٪ است که نشان می‌دهد کلاس غالب، کیفیت مطلوب است و الگوریتم باید توانایی تشخیص اقلیت معیوب را حفظ کند. برای جلوگیری از سوگیری مدل به سمت کلاس اکثریت، در زمان ارزیابی علاوه بر دقت، معیارهای F1 و AUC نیز گزارش شدند تا رفتار مدل روی کلاس اقلیت شفاف بماند."));

  c.push(h2("۳.۲ مجموعه SECOM (نیمه‌هادی)"));
  c.push(bodyPara("مجموعه SECOM از خط تولید نیمه‌هادی با ۱۵۶۷ نمونه و ۵۹۰ ویژگی سنسور است که نرخ پاس تنها ۶.۶۴٪ دارد؛ یعنی تنها حدود ۱۰۴ نمونه در کلاس منفی (خرابی) قرار می‌گیرند. این مجموعه به‌عنوان معیار چالش‌برانگیز برای ارزیابی رفتار مدل در شرایط به‌شدت نامتوازن به کار رفت و با اعمال class_weight متوازن آموزش شد. دقت کلی ۹۶.۴۹٪ و AUC ۰.۹۹۸۱ حاصل شد، اما F1 تنها ۰.۶۴ بود که بازتاب طبیعی سختی تشخیص کلاس اقلیت در داده‌ای با این سطح عدم‌توازن است."));

  c.push(h2("۳.۳ داده مصنوعی"));
  c.push(bodyPara("برای ارزیابی تعمیم‌پذیری مدل در غیاب داده واقعی کافی، یک تولیدکننده داده مصنوعی ساخته شد که ۱۵ پرس، ۳ ترکیب لاستیک، ۱۰۰ قالب، ۲۰۰۰ چرخه پخت و ۲۰٬۰۰۰ قرائت سنسور را با توزیع‌هایی نزدیک به واقعیت تولید می‌کند. نرخ نمونه مثبت در داده مصنوعی ۲۹.۵۵٪ است، یعنی توزیع کلاس نسبت به داده واقعی متعادل‌تر است و در نتیجه مدل فرصت بیشتری برای یادگیری مرز تصمیم بین دو کلاس دارد."));

  // data table
  c.push(new Paragraph({
    keepNext: true, bidirectional: true, alignment: AlignmentType.RIGHT,
    spacing: { before: 200, after: 80 },
    children: [new TextRun({ text: "جدول ۱: مقایسه منابع داده و حجم نمونه", bold: true, size: 22, color: P.tableHeaderBg, rightToLeft: true, font: { ascii: FA_FONT_BOLD, cs: FA_FONT_BOLD } })],
  }));
  c.push(dataTable(
    ["منبع داده", "تعداد نمونه", "تعداد ویژگی", "نرخ مثبت", "نرخ ناهنجاری هدف"],
    [
      ["واقعی (AI4I)", "۱٬۰۰۰", "۷", "۹۷.۷٪", "۵٪"],
      ["مصنوعی", "۲٬۰۰۰", "۷", "۲۹.۶٪", "۵٪"],
      ["SECOM", "۱٬۵۶۷", "۵۹۰", "۶.۶٪", "—"],
    ],
    [25, 18, 18, 18, 21]
  ));

  c.push(h2("۳.۴ پیش‌پردازش"));
  c.push(bodyPara("مرحله پیش‌پردازش در دو ماژول app/db/load_real.py و app/db/seed.py پیاده‌سازی شده است. ابتدا مقادیر گمشده با میانگین ستون جایگزین می‌شوند و سپس ویژگی‌های عددی با StandardScaler استاندارد می‌شوند تا دامنه‌های متفاوت (مثلاً فشار بخار با واحد bar و دما با درجه سانتی‌گراد) به یک مقیاس قابل‌مقایسه تبدیل شوند. برای داده SECOM با ۵۹۰ ویژگی، حذف ستون‌های دارای بیش از ۵۰٪ مقدار گمشده و سپس انتخاب ویژگی بر اساس واریانس انجام شد تا ابعاد کاهش یابد و مدل دچار نفرین بعدی نشود."));
  c.push(bodyPara("برچسب کیفیت به‌صورت باینری تعریف شد: ۱ برای قطعه پذیرفته و ۰ برای قطعه رد. تقسیم آموزش/آزمون با نسبت ۸۰/۲۰ و با ثابت تصادفی RANDOM_STATE=42 انجام شد تا نتایج تکرارپذیر باشند. این ثابت در همه اجراها یکسان نگه داشته شد تا مقایسه بین منابع داده واقعی و مصنوعی معنادار بماند."));

  // ===== Methodology =====
  c.push(h1("۴. روش‌شناسی"));
  c.push(h2("۴.۱ معماری مدل‌ها"));
  c.push(bodyPara("چهار نوع مدل در سامانه TCOP به کار گرفته شده است. نخست، QualityPredictor که یک طبقه‌بند گرادیان‌بویی (Gradient Boosting) است و خروجی احتمال کیفیت مطلوب را برای هر چرخه تولید می‌کند. دوم، AnomalyDetector که بر مبنای جنگل ایزولاسیون (Isolation Forest) چرخه‌های خارج از حد نرمال را با نرخ آلودگی ۵٪ علامت‌گذاری می‌کند. سوم، EnergyPredictor که یک رگرسیون خطی منظم‌شده برای پیش‌بینی مصرف انرژی هر چرخه است. چهارم، CureOptimizer که با ترکیب مدل سینتیک پخت (CureKineticsModel) و مدل انتقال حرارت (HeatTransferModel) زمان بهینه پخت را با هدف رسیدن به درجه پخت ۰.۹۹ و حداقل مصرف انرژی پیدا می‌کند."));

  c.push(h2("۴.۲ متغیرهای ورودی"));
  c.push(bodyPara("مدل کیفیت از هفت ویژگی استفاده می‌کند که در FEATURE_COLS تعریف شده‌اند: مدت زمان چرخه (duration_min)، فشار بخار (steam_pressure)، دمای آب گرم (hot_water_temp)، فشار نیتروژن (nitrogen_pressure)، مصرف انرژی (energy_kwh)، شناسه پرس (press_id) و شناسه قالب (mold_id). دو شناسه آخر به‌صورت رمزگذاری ترتیبی نگاشت شدند تا مدل بتواند اثر یادگیری طولانی‌مدت هر پرس و قالب را بگیرد."));

  c.push(h2("۴.۳ معیارهای ارزیابی"));
  c.push(bodyPara("برای طبقه‌بندی، دقت (Accuracy)، دقت (Precision)، فراخوانی (Recall)، F1 و AUC گزارش شده‌اند. برای رگرسیون انرژی، R² و MAPE به کار رفت. برای مدل فیزیک پخت، درجه پخت نهایی (final_cure_degree)، زمان رسیدن به هدف (time_to_target) و MAPE نسبت به مقادیر ذخیره‌شده در پایگاه داده سنجیده شد. تقسیم آموزش/آزمون ۸۰/۲۰ با random_state ثابت بود."));

  // ===== Results =====
  c.push(h1("۵. نتایج"));
  c.push(h2("۵.۱ مدل کیفیت روی داده واقعی"));
  c.push(bodyPara("مدل روی ۸۰۰ نمونه آموزش و ۲۰۰ نمونه آزمون ارزیابی شد. دقت آزمون ۹۷.۵٪، دقت ۹۷.۹۸٪، فراخوانی ۹۹.۴۹٪، F1 ۹۸.۷۳٪ و AUC ۰.۹۷۸۵ به دست آمد. این یعنی مدل تقریباً تمام قطعه‌های پذیرفته را درست شناسایی می‌کند و تنها ۲.۵٪ از کل پیش‌بینی‌ها نادرست است. دقت بالای آموزش (۹۹.۱۲٪) نسبت به دقت آزمون نشان می‌دهد که مدل بیش‌برازش (overfitting) جزئی دارد، اما با توجه به فاصله اندک، این رفتار پذیرفته است."));

  c.push(new Paragraph({
    keepNext: true, bidirectional: true, alignment: AlignmentType.RIGHT,
    spacing: { before: 200, after: 80 },
    children: [new TextRun({ text: "جدول ۲: معیارهای کامل مدل کیفیت روی سه منبع داده", bold: true, size: 22, color: P.tableHeaderBg, rightToLeft: true, font: { ascii: FA_FONT_BOLD, cs: FA_FONT_BOLD } })],
  }));
  c.push(dataTable(
    ["منبع", "دقت", "Precision", "Recall", "F1", "AUC"],
    [
      ["واقعی (آزمون)", "۹۷.۵٪", "۹۷.۹۸٪", "۹۹.۴۹٪", "۹۸.۷۳٪", "۰.۹۷۸۵"],
      ["مصنوعی (آزمون)", "۹۲.۵٪", "۸۶.۶۷٪", "۸۸.۱۴٪", "۸۷.۳۹٪", "۰.۹۸۰۲"],
      ["SECOM (آموزش)", "۹۶.۴۹٪", "۱۰۰٪", "۴۷.۱۲٪", "۶۴.۰۵٪", "۰.۹۹۸۱"],
    ],
    [22, 14, 16, 14, 14, 20]
  ));

  c.push(h2("۵.۲ مدل کیفیت روی داده مصنوعی"));
  c.push(bodyPara("روی داده مصنوعی، دقت آزمون به ۹۲.۵٪ کاهش یافت که بازتاب توزیع متعادل‌تر کلاس و در نتیجه سختی بیشتر مسئله است. AUC اما به ۰.۹۸۰۲ رسیده، یعنی توانایی رتبه‌بندی مدل بین کلاس‌ها همچنان بالا است و کاهش دقت به انتخاب نقطه آستانه برمی‌گردد نه ضعف مدل. F1 برابر ۸۷.۳۹٪ نشان می‌دهد که تعادل مناسبی بین دقت و فراخوانی برقرار است."));

  c.push(h2("۵.۳ مدل تشخیص ناهنجاری"));
  c.push(bodyPara("هر دو مدل ناهنجاری (واقعی و مصنوعی) با نرخ آلودگی ۵٪ تنظیم شدند و میانگین امتیاز ناهنجاری به‌ترتیب ۰.۴۵۵۲ و ۰.۵۰۵۸ بود. بیشینه امتیاز ناهنجاری ۰.۷۵۶۵ در داده واقعی و ۰.۶۱۷۲ در داده مصنوعی ثبت شد. این مدل برای فعال‌سازی هشدار زودهنگام در داشبورد TCOP به کار خواهد رفت."));

  c.push(h2("۵.۴ مدل‌های فیزیک-محور و انرژی"));
  c.push(bodyPara("مدل سینتیک پخت درجه پخت نهایی ۰.۹۹۰۴ را در زمان هدف ۱۴.۳۲ دقیقه پیش‌بینی کرد و MAPE نسبت به مقادیر ذخیره‌شده برابر ۱۵.۲۹٪ (داده واقعی) و ۴۵.۹۷٪ (داده مصنوعی) بود. این اختلاف قابل انتظار است زیرا داده مصنوعی نویز بیشتری در پارامترهای حرارتی دارد. مدل پیش‌بینی انرژی روی داده واقعی R²=1.0 و MAPE=0 بدست آورد که نشان می‌دهد مصرف انرژی یک تابع قطعی از پارامترهای فرایند در داده واقعی است، در حالی که روی داده مصنوعی R² به ۰.۸۴۳۱ رسید."));

  c.push(chartImage(`${CH}/chart_aux.png`, 470, 468/1300));
  c.push(caption("نمودار ۲: مقایسه نرخ ناهنجاری، R² انرژی و MAPE سینتیک پخت بین داده واقعی و مصنوعی"));

  // ===== Testing & coverage =====
  c.push(h1("۶. تست و پوشش کد"));
  c.push(h2("۶.۱ مجموعه تست"));
  c.push(bodyPara("مجموعه تست شامل ۹۰ آزمون است که در دو دسته unit (هشت فایل) و integration (یک فایل) سازمان‌دهی شده‌اند. آزمون‌های واحد هر ماژول (core/config، models/orm، services/cure_kinetics، services/heat_transfer، services/ml_models، db/load_real و db/seed) را به‌صورت ایزوله پوشش می‌دهند و آزمون یکپارچه‌سازی کل مسیر آموزش تا تولید آرتیفکت را از ابتدا تا انتها اجرا می‌کند. همه ۹۰ آزمون بدون شکست گذر کردند و ۱۲٬۹۵۵ هشدار (عمدتاً مربوط به deprecated شدن utcnow در SQLAlchemy) ثبت شد که بر نتیجه اثری ندارند."));

  c.push(h2("۶.۲ پوشش کد"));
  c.push(bodyPara("میانگین پوشش خط کد سراسر پایگاه ۹۴.۲٪ است که به‌طور قابل‌توجهی از آستانه هدف ۸۰٪ بالاتر است. چهار ماژول (core/config، models/orm، services/cure_kinetics و services/heat_transfer) به پوشش ۱۰۰٪ رسیدند. کمترین پوشش مربوط به db/session با ۷۲٪ است که عمدتاً به مسیرهای مدیریت اتصال اضطراری برمی‌گردد که در محیط آزمون سخت‌تر شبیه‌سازی می‌شوند."));

  c.push(new Paragraph({
    keepNext: true, bidirectional: true, alignment: AlignmentType.RIGHT,
    spacing: { before: 200, after: 80 },
    children: [new TextRun({ text: "جدول ۳: پوشش خط کد به تفکیک ماژول", bold: true, size: 22, color: P.tableHeaderBg, rightToLeft: true, font: { ascii: FA_FONT_BOLD, cs: FA_FONT_BOLD } })],
  }));
  c.push(dataTable(
    ["ماژول", "تعداد خط", "خط پوشش‌نیافته", "درصد پوشش"],
    [
      ["app/core/config.py", "۲۲", "۰", "۱۰۰٪"],
      ["app/models/orm.py", "۸۱", "۰", "۱۰۰٪"],
      ["app/services/cure_kinetics.py", "۲۳", "۰", "۱۰۰٪"],
      ["app/services/heat_transfer.py", "۴۹", "۰", "۱۰۰٪"],
      ["app/services/ml_models.py", "۱۴۳", "۷", "۹۵٪"],
      ["app/db/load_real.py", "۱۳۲", "۱۱", "۹۲٪"],
      ["app/db/seed.py", "۱۱۱", "۹", "۹۲٪"],
      ["app/db/session.py", "۲۵", "۷", "۷۲٪"],
      ["مجموع", "۵۸۶", "۳۴", "۹۴٪"],
    ],
    [38, 18, 22, 22]
  ));

  c.push(chartImage(`${CH}/chart_coverage.png`, 470));
  c.push(caption("نمودار ۳: پوشش تست به تفکیک ماژول؛ خطوط قرمز زیر آستانه هدف و خط چین نارنجی آستانه ۸۰٪"));

  // ===== Analysis =====
  c.push(h1("۷. تحلیل و بحث"));
  c.push(h2("۷.۱ چرا داده واقعی دقت بالاتر داد؟"));
  c.push(bodyPara("دو عامل اصلی برای فاصله ۵ درصدی دقت بین داده واقعی (۹۷.۵٪) و مصنوعی (۹۲.۵٪) وجود دارد. نخست، توزیع کلاس در داده واقعی به‌شدت به سمت کلاس اکثریت (پذیرفته) متمایل است و دقت حساسیت کمتری به خطای روی کلاس اقلیت دارد. دوم، داده واقعی رابطه‌ای نزدیک به قطعی بین پارامترهای فرایند و برچسب دارد که یادگیری آن برای مدل آسان است، در حالی که داده مصنوعی نویز تصادفی هدفمند دارد تا واقعی‌تر باشد. اما این نکته مهم است که AUC روی داده مصنوعی (۰.۹۸۰۲) از داده واقعی (۰.۹۷۸۵) بالاتر است، یعنی توانایی رتبه‌بندی مدل در داده مصنوعی بهتر است و کاهش دقت صرفاً به انتخاب آستانه برمی‌گردد."));

  c.push(h2("۷.۲ چالش SECOM و عدم‌توازن کلاس"));
  c.push(bodyPara("نتایج SECOM چالش کلاسیک یادگیری ماشین در داده‌های به‌شدت نامتوازن را آشکار می‌کند: دقت کلی بالا (۹۶.۴۹٪) اما فراخوانی پایین (۴۷.۱۲٪) زیرا مدل تمایل دارد اکثر نمونه‌ها را در کلاس اکثریت قرار دهد. F1 پایین (۰.۶۴) این پدیده را بازتاب می‌دهد. برای کاربرد واقعی در خط تولید نیمه‌هادی، توصیه می‌شود به‌جای دقت، معیار فراخوانی یا هزینه اقتصادی نادرستی به‌عنوان معیار بهینه‌سازی انتخاب شود و تکنیک‌های SMOTE یا هزینه‌گذاری کلاس اعمال گردد."));

  c.push(h2("۷.۳ توافق مدل یادگیری ماشین و فیزیک"));
  c.push(bodyPara("مدل سینتیک پخت درجه پخت ۰.۹۹۰۴ را پیش‌بینی کرد که در محدوده هدف صنعتی (۰.۹۹ ± ۰.۰۱) قرار دارد. اختلاف MAPE بین داده واقعی (۱۵.۲۹٪) و مصنوعی (۴۵.۹۷٪) نشان می‌دهد که مدل فیزیکی روی پارامترهای واقعی به‌مراتب قابل‌اتکاتر است. این توافق میان پیش‌بینی یادگیری ماشین و مدل فیزیک یک مکانیزم اعتبارسنجی مهم است: چنانچه پیش‌بینی کیفیت مدل ML با پیش‌بینی درجه پخت مدل فیزیک همخوان نباشد، می‌توان آن چرخه را برای بازرسی دستی علامت‌گذاری کرد."));

  c.push(h2("۷.۴ محدودیت‌ها"));
  c.push(bodyPara("سه محدودیت اصلی شناسایی شده است. نخست، حجم داده واقعی (۱۰۰۰ نمونه) برای یادگیری عمیق کافی نیست و به همین دلیل به مدل‌های مبتنی بر درخت (Gradient Boosting) اتکا شد. دوم، نگاشت ویژگی‌های AI4I به متغیرهای دامنه لاستیک یک تقریب است و ممکن است همه وابستگی‌های فیزیکی را پوشش ندهد. سوم، مدل ناهنجاری با نرخ آلودگی ثابت ۵٪ تنظیم شده، در حالی که نرخ واقعی ناهنجاری در خط تولید ممکن است متغیر باشد و نیاز به تنظیم پویا بر اساس داده تاریخی داشته باشد."));

  // ===== Conclusions =====
  c.push(h1("۸. نتیجه‌گیری و توصیه‌ها"));
  c.push(bodyPara("هر دو هدف کلیدی پروژه محقق شد: دقت مدل کیفیت روی داده واقعی به ۹۷.۵٪ رسید (بالاتر از آستانه ۹۰٪) و پوشش تست کد به ۹۴٪ رسید (بالاتر از آستانه ۸۰٪). مدل روی داده مصنوعی نیز دقت ۹۲.۵٪ ثبت کرد که تعمیم‌پذیری روش را در شرایط توزیع متفاوت نشان می‌دهد. آرتیفکت‌های نهایی پنج مدل (quality_real، quality_synthetic، quality_secom، anomaly_real، anomaly_synthetic) ذخیره و کل تغییرات به مخزن GitHub ارسال شد."));

  c.push(h2("۸.۱ توصیه‌های کوتاه‌مدت (۱ تا ۳ ماه)"));
  c.push(bulletItem("استقرار مدل quality_real به‌عنوان مدل پیش‌فرض در API تولید و فعال‌سازی لاگ پیش‌بینی برای همه چرخه‌ها."));
  c.push(bulletItem("افزودن هشدار خودکار در داشبورد TCOP زمانی که امتیاز ناهنجاری از ۰.۷ فراتر می‌رود."));
  c.push(bulletItem("افزایش پوشش ماژول db/session از ۷۲٪ به بالای ۸۵٪ با افزودن آزمون مسیرهای خطای اتصال."));

  c.push(h2("۸.۲ توصیه‌های میان‌مدت (۳ تا ۶ ماه)"));
  c.push(bulletItem("جمع‌آوری داده واقعی اختصاصی لاستیک از سنسورهای پرس برای جایگزینی تدریجی داده AI4I."));
  c.push(bulletItem("آزمون مدل‌های یادگیری عمیق (MLP یا 1D-CNN) زمانی که حجم داده واقعی به بیش از ۱۰٬۰۰۰ چرخه رسید."));
  c.push(bulletItem("اعمال تکنیک SMOTE یا هزینه‌گذاری کلاس برای بهبود فراخوانی روی داده نامتوازن مشابه SECOM."));
  c.push(bulletItem("پیاده‌سازی تنظیم پویای نرخ آلودگی مدل ناهنجاری بر اساس داده تاریخی سه‌ماهه اخیر."));

  c.push(h2("۸.۳ توصیه‌های بلندمدت (۶ تا ۱۲ ماه)"));
  c.push(bulletItem("ادغام پیش‌بینی کیفیت با مدل بهینه‌سازی زمان پخت تا زمان هر چرخه به‌صورت خودکار بر اساس پیش‌بینی کیفیت تنظیم شود."));
  c.push(bulletItem("ساخت حلقه بازخورد: هر بار که اپراتور برچسب واقعی یک قطعه را وارد می‌کند، مدل به‌صورت آنلاین به‌روزرسانی شود."));
  c.push(bulletItem("انتشار داشبورد بلادرنگ برای مدیریت تولید با شاخص‌های OEE و ضریب بازده کیفیت لحظه‌ای."));

  // ===== Appendix =====
  c.push(h1("پیوست: مشخصات آرتیفکت‌ها"));
  c.push(bodyPara("پنج آرتیفکت مدل و یک گزارش آموزش JSON در مسیر backend/app/ml/artifacts/ ذخیره شده‌اند. جدول زیر اندازه فایل و تاریخ آخرین به‌روزرسانی هر آرتیفکت را نشان می‌دهد."));

  c.push(new Paragraph({
    keepNext: true, bidirectional: true, alignment: AlignmentType.RIGHT,
    spacing: { before: 200, after: 80 },
    children: [new TextRun({ text: "جدول ۴: مشخصات آرتیفکت‌های مدل نهایی", bold: true, size: 22, color: P.tableHeaderBg, rightToLeft: true, font: { ascii: FA_FONT_BOLD, cs: FA_FONT_BOLD } })],
  }));
  c.push(dataTable(
    ["نام فایل", "نوع مدل", "حجم (KB)", "تاریخ به‌روزرسانی"],
    [
      ["quality_real.pkl", "Gradient Boosting (واقعی)", "۱۷۴", "۱۴۰۵/۰۹/۰۲ ۰۷:۴۷"],
      ["quality_synthetic.pkl", "Gradient Boosting (مصنوعی)", "۲۵۸", "۱۴۰۵/۰۹/۰۲ ۰۷:۴۷"],
      ["quality_secom.pkl", "Gradient Boosting (SECOM)", "۳۴۴", "۱۴۰۵/۰۹/۰۲ ۰۷:۴۷"],
      ["anomaly_real.pkl", "Isolation Forest (واقعی)", "۲٬۴۹۶", "۱۴۰۵/۰۹/۰۲ ۰۷:۴۷"],
      ["anomaly_synthetic.pkl", "Isolation Forest (مصنوعی)", "۳٬۴۳۶", "۱۴۰۵/۰۹/۰۲ ۰۷:۴۷"],
      ["train_report.json", "گزارش آموزش", "۵", "۱۴۰۵/۰۹/۰۲ ۰۷:۴۷"],
    ],
    [28, 32, 18, 22]
  ));

  c.push(bodyPara("همه آرتیفکت‌ها با ثابت تصادفی RANDOM_STATE=42 و تقسیم آموزش/آزمون ۸۰/۲۰ تولید شده‌اند تا نتایج تکرارپذیر باشند. برای بارگذاری مدل در محیط تولید، از تابع load_artifact در ماژول app/ml/inference استفاده شود."));

  return c;
}

// ── DOCUMENT ──
const doc = new Document({
  styles: {
    default: {
      document: {
        run: {
          font: { ascii: FA_FONT, eastAsia: FA_FONT, cs: FA_FONT },
          size: 24, color: "000000",
        },
        paragraph: { spacing: { line: 360 } },
      },
    },
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 11906, height: 16838 },
          margin: { top: 0, bottom: 0, left: 0, right: 0 },
        },
      },
      children: buildCover(),
    },
    {
      properties: {
        type: SectionType.NEXT_PAGE,
        page: {
          size: { width: 11906, height: 16838 },
          margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 },
          pageNumbers: { start: 1, formatType: "decimal" },
        },
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            bidirectional: true, alignment: AlignmentType.RIGHT,
            children: [new TextRun({
              text: "گزارش آموزش مدل‌های هوش مصنوعی — سامانه TCOP",
              size: 18, color: "808080", rightToLeft: true,
              font: { ascii: FA_FONT, cs: FA_FONT },
            })],
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "808080" })],
          })],
        }),
      },
      children: buildBody(),
    },
  ],
});

Packer.toBuffer(doc).then(buf => {
  const out = "/home/z/my-project/download/ML_Training_Report_TCOP.docx";
  fs.writeFileSync(out, buf);
  console.log("WROTE", out, buf.length, "bytes");
}).catch(e => { console.error("ERR", e); process.exit(1); });

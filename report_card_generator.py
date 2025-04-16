# report_card_generator.py

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from bidi.algorithm import get_display
import arabic_reshaper
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import ttfonts
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(TTFont('IranSans', 'fonts/IRANSans.ttf'))
import os

# ثبت فونت
font_path = os.path.join("fonts", "Vazir.ttf")
pdfmetrics.registerFont(TTFont("Vazir", font_path))

def reshape_text(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def generate_report_card(student_name, student_level, grades_df, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # نام دانش‌آموز
    c.setFont("Vazir", 14)
    c.drawRightString(width - 40, height - 50, reshape_text(f"نام دانش‌آموز: {student_name}"))

    # پایه‌ی تحصیلی
    c.drawRightString(width - 40, height - 80, reshape_text(f"پایه: {student_level}"))

    # تیتر جدول
    c.setFont("Vazir", 12)
    c.drawRightString(width - 40, height - 120, reshape_text("لیست نمرات:"))

    y = height - 150
    c.setFont("Vazir", 11)

    table_data = [[
    get_display(reshape_text("نمره")),
    get_display(reshape_text("نام گروه")),
    get_display(reshape_text("رتبه در گروه")),
    get_display(reshape_text("رتبه کل"))
]]

    # افزودن سطرهای اطلاعاتی
    for _, row in grades_df.iterrows():
        table_data.append([
            row['score'],
            str(row['group']),
            int(row['rank_in_group']),
            int(row['rank_in_lesson']),
        ])

    # ساخت جدول
    table = Table(table_data, colWidths=[60, 100, 90, 80])

    # استایل جدول
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'IranSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))

    # نمایش جدول در موقعیت مناسب روی صفحه
    table.wrapOn(c, width, height)
    table.drawOn(c, 40, y - (20 * len(table_data)))  # y موقعیت پایین جدول

    c.save()
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
import os

# ثبت فونت
pdfmetrics.registerFont(TTFont('IranSans', 'fonts/IRANSans.ttf'))
font_path = os.path.join("fonts", "Vazir.ttf")
pdfmetrics.registerFont(TTFont("Vazir", font_path))

def reshape_text(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


def generate_report_card(student_name, student_level, grades_df, output_path , config_dict):
    
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # دریافت اطلاعات کانفیگ
    # آماده‌سازی اطلاعات برای جدول دو سطری و چهار ستونی (کلید - مقدار)
    # آماده‌سازی اطلاعات جدول با ترتیب ستون از راست به چپ
    info_data = [
        [reshape_text("نام موسسه"), reshape_text(str(config_dict.get("school_name", ""))),
        reshape_text("شماره آزمون"), reshape_text(str(config_dict.get("exam_number", "")))][::-1],
        [reshape_text("تاریخ آزمون"), reshape_text(str(config_dict.get("exam_date", ""))),
        reshape_text("سقف نمره"), reshape_text(str(config_dict.get("score_max", "")))][::-1]
    ]

    col_widths = [150, 100, 150, 100]  # دو جفت ستون کلید و مقدار
    info_table = Table(info_data, colWidths=col_widths)

    # استایل‌دهی
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'IranSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # حاشیه نازک برای همه سلول‌ها
        ('BOX', (0, 0), (-1, -1), 1, colors.black),   # حاشیه ضخیم بیرونی
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),  # راست‌چین‌سازی
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))

    # موقعیت جدول: بالای صفحه
    table_width = sum(col_widths)
    x = width - table_width - 40  # راست‌چین با فاصله ۴۰ از راست
    y = height - 100              # فاصله از بالای صفحه

    info_table.wrapOn(c, width, height)
    info_table.drawOn(c, x, y)

    next_content_y = y - 30  # برای مثال، ادامه‌ی محتوا از اینجا شروع می‌شه

    # نام دانش‌آموز
    c.setFont("Vazir", 14)
    c.drawRightString(width - 40, next_content_y, reshape_text(f"نام دانش‌آموز: {student_name}"))
    next_content_y -= 30 

    # پایه‌ی تحصیلی
    c.drawRightString(width - 40, next_content_y, reshape_text(f"پایه: {student_level}"))
    next_content_y -= 30

    # تیتر جدول
    c.setFont("Vazir", 12)
    c.drawRightString(width - 40, next_content_y, reshape_text("کارنامه:"))
    next_content_y -= 100


    c.setFont("Vazir", 11)

    table_data = [[
    reshape_text("نام درس"),
    reshape_text("نام گروه"),
    reshape_text("نمره"),
    reshape_text("ضریب"),
    reshape_text("درصد"),
    reshape_text("رتبه در درس"),
    reshape_text("رتبه کل")
    ]][0][::-1]

    table_data = [table_data]

    sum_factor = 0
    # افزودن سطرهای اطلاعاتی
    for _, row in grades_df.iterrows():
        lesson_name = reshape_text(str(row['lesson_name']))
        group = reshape_text(str(row['group']))
        rank_in_group = str(row['rank_in_group'])
        score = str(row['score'])
        factor = str(row['factor'])
        sum_factor += row['factor']
        percent = str(row['score'] / config_dict.get("score_max", "") * 100)
        rank_in_lesson = str(row['rank_in_lesson'])

        row_data = [lesson_name,group , score , factor , percent , rank_in_group, rank_in_lesson][::-1]
        table_data.append(row_data)

    summary_row = [
        "",  # نام درس
        "",
        str(reshape_text(f"نمره کل: {round(row['weighted_avg'], 1)}")),
        sum_factor, #مجموع ضرایب,
        str(round(row['weighted_avg'] / config_dict.get("score_max", "") * 100 , 1)),
        "",
        str(reshape_text(f"رتبه کل در پایه: {row['rank_in_level']}"))
    ][::-1]  # ترتیب RTL

    table_data.append(summary_row)
    # ساخت جدول
    table = Table(table_data, colWidths=[60 , 60, 60 ,60, 60, 100, 120])

    # استایل جدول
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'IranSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('SPAN', (0, -1), (1, -1)),  # نمره کل
        ('SPAN', (4, -1), (5, -1)),  # رتبه کل در پایه
    ]))

    # نمایش جدول در موقعیت مناسب روی صفحه
    table.wrapOn(c, width, height)
    table.drawOn(c, 40, next_content_y - (20 * len(table_data)))  # y موقعیت پایین جدول

    c.save()
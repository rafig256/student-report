# report_card_generator.py

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from bidi.algorithm import get_display
import arabic_reshaper
import os

def reshape_text(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def generate_report_card(student_name, student_level, grades_df, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # نام دانش‌آموز
    c.setFont("Helvetica", 14)
    c.drawRightString(width - 40, height - 50, reshape_text(f"نام دانش‌آموز: {student_name}"))

    # پایه‌ی تحصیلی
    c.drawRightString(width - 40, height - 80, reshape_text(f"پایه: {student_level}"))

    # تیتر جدول
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(width - 40, height - 120, reshape_text("لیست نمرات:"))

    y = height - 150
    c.setFont("Helvetica", 11)

    for _, row in grades_df.iterrows():
        lesson_name = reshape_text(str(row['lesson_name']))
        score = row['score']
        rank_in_group = row['rank_in_group']
        c.drawRightString(width - 40, y, f"{lesson_name} | نمره: {score} | رتبه در گروه: {rank_in_group}")
        y -= 20

    c.save()

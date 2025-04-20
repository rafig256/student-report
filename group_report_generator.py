# group_report_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import arabic_reshaper
from bidi.algorithm import get_display
import os

# ثبت فونت
pdfmetrics.registerFont(TTFont("Vazir", os.path.join("fonts", "Vazir.ttf")))

def reshape_text(text):
    if not isinstance(text, str):
        text = str(text)
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def generate_group_report(group_df, output_path, group_name):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    c.setFont("Vazir", 14)
    title_text = reshape_text(f"گزارش نمرهات گروه {group_name}")
    c.drawRightString(width - 50, height - 50, title_text)

    table_data = [
        [reshape_text("نام"), reshape_text("نام درس"), reshape_text("نمره"), reshape_text("ضریب"), reshape_text("رتبه در گروه"), reshape_text("میانگین کل")]
    ]

    for _, row in group_df.iterrows():
        table_data.append([
            reshape_text(row["name"]),
            reshape_text(row["lesson_name"]),
            row["score"],
            row["factor"],
            row["rank_in_group"],
            f"{row['weighted_avg']:.2f}"
        ])

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Vazir'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    table.wrapOn(c, width, height)
    table.drawOn(c, 30, height - 100 - 18 * len(table_data))

    c.showPage()
    c.save()
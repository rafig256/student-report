import pandas as pd
from report_card_generator import generate_report_card
import os

output_dir = "report_output"
# خواندن داده‌ها از فایل اکسل
students = pd.read_excel("sample-data.xlsx", sheet_name="students")
students_dict = students.set_index("id").to_dict(orient="index")
lessons = pd.read_excel("sample-data.xlsx", sheet_name="lessons")
student_lesson = pd.read_excel("sample-data.xlsx", sheet_name="student_lesson")
grades = pd.read_excel("sample-data.xlsx", sheet_name="grades")
config_df = pd.read_excel("sample-data.xlsx", sheet_name='config')

config_dict = dict(zip(config_df['key'], config_df['value']))

grades_full = grades \
    .merge(students, left_on="st_id", right_on="id") \
    .merge(lessons[['id', 'name', 'level', 'factor']].rename(columns={'name': 'lesson_name'}), \
    left_on="l_id", right_on="id", suffixes=("_student", "_lesson")) \
    .merge(student_lesson[['st_id', 'l_id', 'group']], on=["st_id", "l_id"])

grades_full['rank_in_group'] = grades_full.groupby(['l_id','group'])['score'] \
    .rank(method='dense', ascending=False).astype(int)

grades_full['rank_in_lesson'] = grades_full.groupby('l_id')['score'] \
    .rank(method='dense', ascending=False).astype(int)

grades_full['weighted_score'] = grades_full['score'] * grades_full['factor']

# میانگین نمرات بر حسب ضرایب
weighted_avg = grades_full.groupby(['st_id', 'level_student'], group_keys=False).apply(
    lambda df: pd.Series({
        'total_weighted': (df['score'] * df['factor']).sum(),
        'total_factors': df['factor'].sum()
    })
).reset_index()

weighted_avg['weighted_avg'] = weighted_avg['total_weighted'] / weighted_avg['total_factors']

# محاسبه‌ی رتبه در پایه
weighted_avg['rank_in_level'] = weighted_avg.groupby('level_student')['weighted_avg'] \
    .rank(method='dense', ascending=False)

grades_full = grades_full.merge(
    weighted_avg[['st_id', 'rank_in_level', 'weighted_avg']],
    on='st_id'
)


for student_id, student_data in grades_full.groupby("st_id"):
    student_info = students_dict.get(student_id, {})
    output_path = os.path.join(output_dir, f"{student_info.get('name', student_id)}.pdf")
    generate_report_card(student_data, output_path, config_dict, student_info)

print("تمام کارنامه‌ها ساخته شدند.")

# ذخیره فایل اکسل داخل پوشه report
grades_full.to_excel("report_output/grades_report.xlsx", index=False)
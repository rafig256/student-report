import pandas as pd

# خواندن داده‌ها از فایل اکسل
students = pd.read_excel("sample-data.xlsx", sheet_name="students" ,usecols="A,B,F")
lessons = pd.read_excel("sample-data.xlsx", sheet_name="lessons")
student_lesson = pd.read_excel("sample-data.xlsx", sheet_name="student_lesson")
grades = pd.read_excel("sample-data.xlsx", sheet_name="grades")

grades_full = grades \
    .merge(students, left_on="st_id", right_on="id") \
    .merge(lessons[['id','level','factor']], left_on="l_id", right_on="id", suffixes=("_student", "_lesson")) \
    .merge(student_lesson[['st_id', 'l_id', 'group']], on=["st_id", "l_id"])

grades_full['rank_in_group'] = grades_full.groupby(['l_id','group'])['score'] \
    .rank(method='dense', ascending=False).astype(int)

grades_full['rank_in_lesson'] = grades_full.groupby('l_id')['score'] \
    .rank(method='dense', ascending=False).astype(int)

grades_full['weighted_score'] = grades_full['score'] * grades_full['factor']

weighted_avg = grades_full.groupby(['st_id', 'level_student']).apply(
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

# ذخیره فایل اکسل داخل پوشه report
grades_full.to_excel("report_output/grades_report.xlsx", index=False)
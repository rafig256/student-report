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

print (grades_full)
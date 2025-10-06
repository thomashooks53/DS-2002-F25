import csv
import json
import pandas as pd

data = [
    {"student_id": 101, "major": "Computer Science", "GPA": 3.8, "is_cs_major": "Yes", "credits_taken": "15.0"},
    {"student_id": 102, "major": "Mathematics", "GPA": 3, "is_cs_major": "No", "credits_taken": "12.5"},
    {"student_id": 103, "major": "Biology", "GPA": 2.9, "is_cs_major": "No", "credits_taken": "10"},
    {"student_id": 104, "major": "Computer Science", "GPA": 4, "is_cs_major": "Yes", "credits_taken": "18.0"},
    {"student_id": 105, "major": "Physics", "GPA": 3.5, "is_cs_major": "No", "credits_taken": "14.5"}
]

headers = ["student_id", "major", "GPA", "is_cs_major", "credits_taken"]
with open("raw_survey_data.csv", "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    for row in data:
        writer.writerow(row)


courses = [
    {
        "course_id": "DS2002",
        "section": "001",
        "title": "Data Science Systems",
        "level": 200,
        "instructors": [
            {"name": "Austin Rivera", "role": "Primary"},
            {"name": "Heywood Williams-Tracy", "role": "TA"}
        ]
    },
    {
        "course_id": "CHEM3410",
        "section": "200",
        "title": "Phys Chem - Quantum Theory",
        "level": 300,
        "instructors": [
            {"name": "Dr. Ian Harrison", "role": "Primary"},
            {"name": "Chrissy Blondin", "role": "TA"}
        ]
    },
    {
        "course_id": "BIOL3000",
        "section": "100",
        "title": "Cell Biology",
        "level": 300,
        "instructors": [
            {"name": "Dr. Mike Wormington", "role": "Primary"},
            {"name": "Ellie Smith", "role": "TA"}
        ]
    },
    {
        "course_id": "CHEM3721",
        "section": "101",
        "title": "Analytical Chemistry Lab",
        "level": 300,
        "instructors": [
            {"name": "Dr. Rebecca Pompano", "role": "Primary"},
            {"name": "Wisdom Owusu", "role": "TA"}
        ]
    },
    {
        "course_id": "CHEM4410",
        "section": "001",
        "title": "Biological Chemistry 1",
        "level": 400,
        "instructors": [
            {"name": "Andreas Gahlmann", "role": "Primary"},
            {"name": "Linda Columbus", "role": "Primary"},
            {"name": "Rachel Stegmeier", "role": "TA"}
        ]
    }
]

with open("raw_course_catalog.json", "w") as f:
    json.dump(courses, f, indent=4)

df = pd.read_csv("raw_survey_data.csv")
df["is_cs_major"] = df["is_cs_major"].replace({"Yes": True, "No": False})
df = df.astype({"GPA": "float64", "credits_taken": "float64"})
df.to_csv("clean_survey_data.csv", index=False)

with open("raw_course_catalog.json", "r") as f:
    data = json.load(f)
df_courses = pd.json_normalize(data, record_path=['instructors'], meta=['course_id', 'title', 'level'])
df_courses.to_csv("clean_course_catalog.csv", index=False)
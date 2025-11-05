import sqlite3
DB_PATH = "school.db"

class Teacher:
    def __init__(self, teacher_id, name):
        self.teacher_id = teacher_id
        self.name = name
        self.classes_taught = []

    def add_class(self, course):
        self.classes_taught.append(course)

    def add_grade(self, course, student, grade):
        if course in self.classes_taught:
            course.assign_grade(student, grade)

            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO grades (student_id, course_id, grade) VALUES (?, ?, ?);",
                (student.student_id, course.course_id, grade)
            )
            conn.commit()
            conn.close()
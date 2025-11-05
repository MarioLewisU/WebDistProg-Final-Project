from models.course import Course
import sqlite3
DB_PATH = "school.db"

class Admin:
    def __init__(self,name):
        self.name = name

    def create_class(self, course_id, name, teacher=None):
        course = Course(course_id, name, teacher)
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            teacher_id = teacher.teacher_id if teacher else None
            cur.execute(
                "INSERT OR IGNORE INTO courses (id, name, teacher_id) VALUES (?, ?, ?);",
                (course.course_id, course.name, teacher_id)
            )
            conn.commit()
        return course

    def add_student_to_class(self, student, course):
        course.add_student(student)
        student.add_class(course)
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT OR IGNORE INTO enrollments (student_id, course_id) VALUES (?, ?);",
                (student.student_id, course.course_id)
            )
            conn.commit()

    def remove_student_from_class(self, student, course):
        course.remove_student(student)
        student.drop_class(course)
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM enrollments WHERE student_id=? AND course_id=?;",
                (student.student_id, course.course_id)
            )
            conn.commit()
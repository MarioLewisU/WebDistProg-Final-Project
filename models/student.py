import sqlite3
DB_PATH = "school.db"
class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.classes_enrolled = []
        self.grades = {}

    def add_class(self,course):
        self.classes_enrolled.append(course)

    def drop_class(self,course):
        self.classes_enrolled.remove(course)

    def view_grades(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT g.grade, c.name as course_name
            FROM grades g
            JOIN courses c ON g.course_id = c.id
            WHERE g.student_id = ?
            ORDER BY c.name
        """, (self.student_id,))
        rows = cur.fetchall()
        conn.close()

        grades_by_course = {}
        for row in rows:
            grades_by_course.setdefault(row['course_name'], []).append(row['grade'])

        return grades_by_course

    def calculate_gpa(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT g.grade, c.name as course_name
            FROM grades g
            JOIN courses c ON g.course_id = c.id
            WHERE g.student_id = ?
        """, (self.student_id,))
        rows = cur.fetchall()
        conn.close()

        grades_by_course = {}
        for row in rows:
            grades_by_course.setdefault(row['course_name'], []).append(row['grade'])

        total_points = 0
        total_classes = 0

        for grades in grades_by_course.values():
            if grades:
                average = sum(grades) / len(grades)

                if 97 <= average <= 100:
                    points = 4.0
                elif 93 <= average < 97:
                    points = 4.0
                elif 90 <= average < 93:
                    points = 3.7
                elif 87 <= average < 90:
                    points = 3.3
                elif 83 <= average < 87:
                    points = 3.0
                elif 80 <= average < 83:
                    points = 2.7
                elif 77 <= average < 80:
                    points = 2.3
                elif 73 <= average < 77:
                    points = 2.0
                elif 70 <= average < 73:
                    points = 1.7
                elif 67 <= average < 70:
                    points = 1.3
                elif 63 <= average < 67:
                    points = 1.0
                elif 60 <= average < 63:
                    points = 0.7
                else:
                    points = 0.0

                total_points += points
                total_classes += 1

        return round(total_points / total_classes, 2) if total_classes > 0 else 0.0
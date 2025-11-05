from models.student import Student
from models.course import Course
from models.teacher import Teacher
from models.admin import Admin
import sqlite3

DB_PATH = "school.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    with get_conn() as conn:
        cur = conn.cursor()


        # teacher table creation
        cur.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
        """)


        # courses table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                teacher_id INTEGER,
                FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE SET NULL
            );
        """)


        # students
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
        """)


        # enrollments table

        cur.execute("""
            CREATE TABLE IF NOT EXISTS enrollments (
                student_id INTEGER,
                course_id INTEGER,
                PRIMARY KEY(student_id, course_id),
                FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY(course_id) REFERENCES courses(id) ON DELETE CASCADE
            );
        """)


        # grades
        cur.execute("""
            CREATE TABLE IF NOT EXISTS grades (
                student_id INTEGER,
                course_id INTEGER,
                grade REAL,
                FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY(course_id) REFERENCES courses(id) ON DELETE CASCADE
            );
        """)
        conn.commit()

class Overview:
    def __init__(self):
        init_db()

        self.admin = Admin("Principal")
        
        self.teachers = [
            Teacher(1, "Mr. Johnson"),
            Teacher(2, "Mr. Smith"),
            Teacher(3, "Mrs. Jamie"),
            Teacher(4, "Mrs. Kelly"),
            Teacher(5, "Mrs. Daniels"),
        ]

        self.courses = [
            self.admin.create_class(1, "English 101", self.teachers[0]),
            self.admin.create_class(2, "Math 102", self.teachers[1]),
            self.admin.create_class(3, "Science 103", self.teachers[2]),
            self.admin.create_class(4, "History 104", self.teachers[3]),
            self.admin.create_class(5, "Physical Education", self.teachers[4])
        ]
       
        for course in self.courses:
            course.teacher.add_class(course)

        self.students = [
            Student(1, "John Cena"),
            Student(2, "Jon Jones"),
            Student(3, "Steve Austin"),
            Student(4, "Conor McGregor"),
            Student(5, "Jeff Hardy")
        ]

                #had ai preload some data python mem
        preload_data = [
            (0, [0, 1, 2, 3]),
            (1, [0, 1, 3, 4]),
            (2, [0, 2, 3, 4]),
            (3, [0, 1, 2, 4]),
            (4, [1, 2, 3, 4])
        ]

        for student_idx, course_indices in preload_data:
            student = self.students[student_idx]
            for c_idx in course_indices:
                course = self.courses[c_idx]
                student.add_class(course)
                course.add_student(student)

        self.seed_db()

    def seed_db(self):
        with get_conn() as conn:
            cur = conn.cursor()

            
            for teacher in self.teachers:
                cur.execute(
                    "INSERT OR IGNORE INTO teachers (id, name) VALUES (?, ?);",
                    (teacher.teacher_id, teacher.name)
                )

            
            for course in self.courses:
                cur.execute(
                    "INSERT OR IGNORE INTO courses (id, name, teacher_id) VALUES (?, ?, ?);",
                    (course.course_id, course.name, course.teacher.teacher_id)
                )

            
            for student in self.students:
                cur.execute(
                    "INSERT OR IGNORE INTO students (id, name) VALUES (?, ?);",
                    (student.student_id, student.name)
                )

            
            for student in self.students:
                for course in student.classes_enrolled:
                    cur.execute(
                        "INSERT OR IGNORE INTO enrollments (student_id, course_id) VALUES (?, ?);",
                        (student.student_id, course.course_id)
                    )

            for student in self.students:
                for course_name, grades in student.grades.items():
                    course = next((c for c in self.courses if c.name == course_name), None)
                    if course:
                        for grade in grades:
                            cur.execute(
                                "INSERT INTO grades (student_id, course_id, grade) VALUES (?, ?, ?);",
                                (student.student_id, course.course_id, grade)
                            )
            conn.commit()

    def find_student(self, student_id):
        student = next((s for s in self.students if s.student_id == student_id), None)
        if student:
            return student
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM students WHERE id=?", (student_id,))
            row = cur.fetchone()
            if row:
                return Student(row['id'], row['name'])
        return None
        
    def find_class(self, course_id):
        course = next((c for c in self.courses if c.course_id == course_id), None)
        if course:
            return course
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT c.id, c.name, t.id as teacher_id, t.name as teacher_name
                FROM courses c
                LEFT JOIN teachers t ON c.teacher_id = t.id
                WHERE c.id=?
            """, (course_id,))
            row = cur.fetchone()
            if row:
                teacher = self.find_teacher(row['teacher_id'])
                return Course(row['id'], row['name'], teacher)
        return None
    
    def find_teacher(self, teacher_id):
        teacher = next((t for t in self.teachers if t.teacher_id == teacher_id), None)
        if teacher:
            return teacher
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM teachers WHERE id=?", (teacher_id,))
            row = cur.fetchone()
            if row:
                return Teacher(row['id'], row['name'])
        return None
        
    def show_students(self):
        print("Students:")
        for student in self.students:
            print(f"ID: {student.student_id}, Name: {student.name}")
    
    def show_classes(self):
        print("Classes:")
        for course in self.courses:
            print(f"ID: {course.course_id}, Name: {course.name}")

    def run(self):
        while True:
            print("Welcome to the login portal!")
            position = input("Who will be using the portal today? (admin, teacher, student, or exit): ").lower()

            if position == "admin":
                password = input("Enter admin password: ")
                if password == "admin123":
                    self.admin_menu()
                else:
                    print("Access Denied. Please try again.")

            elif position == "teacher":
                self.teacher_menu()

            elif position == "student":
                self.student_menu()

            elif position == "exit":
                print("Goodbye!")
                break

            else:
                print("Invalid reply, try again.")

    def admin_menu(self):
        print("Admin please review the following.")
        while True:
            print("1. Add student")
            print("2. Create a class")
            print("3. Add student to class")
            print("4. Remove student from class")
            print("5. Modify student grades")
            print("6. View students GPA")
            print("7. View students")
            print("8. Exit Menu")
            option = input("Enter an option: ")

            if option == "1":
                name = input("Enter the student you would like to add (First + Last): ")
                student_id = len(self.students) + 1
                student = Student(student_id, name)
                student.grades = {}
                self.students.append(student)
                with get_conn() as conn:
                    cur = conn.cursor()
                    cur.execute(
                        "INSERT OR IGNORE INTO students (id, name) VALUES (?, ?);",
                        (student.student_id, student.name)
                    )
                    conn.commit()
                    print(f"Student {name} has been added with an ID of {student_id}")

            elif option == "2":
                course_id = len(self.courses) + 1
                name = input("Enter the class you would like to create: ")
                course = Course(course_id, name)  
                self.courses.append(course)

                
                with get_conn() as conn:
                    cur = conn.cursor()
                    cur.execute(
                        "INSERT OR IGNORE INTO courses (id, name, teacher_id) VALUES (?, ?, ?);",
                        (course.course_id, course.name, None)
                    )
                    conn.commit()

                print(f"{name} has been created as a class with an ID of {course_id}")

            elif option == "3":
                print("Students:")
                for student in self.students:
                    print(f"ID: {student.student_id}, Name: {student.name}")

                print("Classes:")
                for course in self.courses:
                    print(f"ID: {course.course_id}, Name: {course.name}")

                student_id_input = int(input("Enter the student's ID: "))
                course_id_input = int(input("Enter the class ID: "))

                student = self.find_student(student_id_input)
                course = self.find_class(course_id_input)

                if student and course:
                    student.add_class(course)
                    course.add_student(student)

                    with get_conn() as conn:
                        cur = conn.cursor()
                        cur.execute(
                            "INSERT OR IGNORE INTO enrollments (student_id, course_id) VALUES (?, ?);",
                            (student.student_id, course.course_id)
                        )
                        conn.commit()

                    print(f"{student.name} has been added to {course.name}")
                else:
                    print("Invalid student or class ID")
                    
            elif option == "4":
                print("Students:")
                for student in self.students:
                    print(f"ID: {student.student_id}, Name: {student.name}")

                print("Classes:")
                for course in self.courses:
                    print(f"ID: {course.course_id}, Name: {course.name}")

                student_id_input = int(input("Enter the student's ID: "))
                course_id_input = int(input("Enter the class ID: "))

                student = self.find_student(student_id_input)
                course = self.find_class(course_id_input)

                if student and course:
                    student.drop_class(course)
                    course.remove_student(student)

                    with get_conn() as conn:
                        cur = conn.cursor()
                        cur.execute(
                            "DELETE FROM enrollments WHERE student_id=? AND course_id=?;",
                            (student.student_id, course.course_id)
                        )
                        conn.commit()

                    print(f"{student.name} has been removed from {course.name}")
                else:
                    print("Invalid student or class ID")


            elif option == "5":
                print("Students:")
                for s in self.students:
                    print(f"ID: {s.student_id}, Name: {s.name}")

                student_id = int(input("Enter the student ID to modify grades: "))
                student = self.find_student(student_id)

                if student and student.classes_enrolled:
                    for course in student.classes_enrolled:
                        grade = float(input(f"Enter numeric grade for {student.name} in {course.name}: "))
                        student.grades.setdefault(course.name, [])
                        student.grades[course.name].append(grade)

                        with get_conn() as conn:
                            cur = conn.cursor()
                            cur.execute(
                                "INSERT INTO grades (student_id, course_id, grade) VALUES (?, ?, ?);",
                                (student.student_id, course.course_id, grade)
                            )
                            conn.commit()

                    print("Grades have been updated.")
                elif student:
                    print(f"{student.name} is not enrolled in any classes yet.")
                else:
                    print("Student cannot be found.")


            elif option == "6":
                self.show_students()
                studentid = int(input("Enter student ID to view final GPA: "))
                student = self.find_student(studentid)
                if student:
                    gpa = student.calculate_gpa()
                    print(f"Final GPA for {student.name} is {gpa}")
                else:
                    print("Student cannot be found.")

            elif option == "7":
                self.show_students()

            elif option == "8":
                print("Exiting admin portal.")
                return
            
    def teacher_menu(self): 

        print("Confirm you are a current student teacher.")
        for teacher in self.teachers:
            print(f"ID: {teacher.teacher_id}, Name: {teacher.name}")

        teacher_id_input = int(input("Enter your teacher ID to log in: "))
        teacher = self.find_teacher(teacher_id_input)

        if teacher is None:
            print("No longer teaching here.")
            return
        
        while True:
            print(f"Welcome {teacher.name}")
            print("1. View classes being taught")
            print("2. View my students")
            print("3. Grade Assigning")
            print("4. Exit Menu")
            option = input("Enter a desired number option: ")


            if option == "1":
                print(f"These are the classes taught by {teacher.name}:")
                teacher_classes = [course for course in self.courses if course.teacher == teacher]
                if teacher_classes:
                    for course in teacher_classes:
                        print(f"ID: {course.course_id}, Name: {course.name}")
                else:
                    print("You're not teaching any classes, sorry.")

            elif option == "2":
                print("Below are the students in your class: ")
                teacher_classes = [course for course in self.courses if course.teacher == teacher]
                for course in teacher_classes:
                    print(f"Class: {course.name}")
                    if course.students:
                        for student in course.students:
                            print(f"{student.name}")
                    else:
                        print("No students enrolled.")

            elif option == "3":
                print(f"{teacher.name}'s Grade Book")
                teacher_classes = [course for course in self.courses if course.teacher == teacher]
                for course in teacher_classes:
                    print(f"Class: {course.name}")
                    if course.students:
                        for student in course.students:
                            grade = float(input(f"Enter numerical grade for {student.name} in {course.name}: "))
                            student.grades.setdefault(course.name, [])
                            student.grades[course.name].append(grade)

                            with get_conn() as conn:
                                cur = conn.cursor()
                                cur.execute(
                                    "INSERT INTO grades (student_id, course_id, grade) VALUES (?, ?, ?);",
                                    (student.student_id, course.course_id, grade)
                                )
                                conn.commit()

                        print(f"Grades for {course.name} have been updated.")
                    else:
                        print("No students in this class")

            elif option == "4":
                print("Exiting teacher portal.")
                return

            else:
                print("Invalid option, try again")

    def student_menu(self):
        print("Hello, please select your student ID to continue")
        for student in self.students:
            print(f"ID: {student.student_id}, Name: {student.name}")
            
        student_id_input = int(input("Enter your student ID to login: "))
        student = self.find_student(student_id_input)

        if student is None:
            print("Student is not here anymore.")
            return
        
        while True:
            print(f"Welcome {student.name}")
            print("1. View classes")
            print("2. View grades")
            print("3. View GPA")
            print("4. Add class")
            print("5. Drop class")
            print("6. Exit")

            option = input("Enter a desired number option: ")  

            if option == "1":
                student_classes = [course for course in self.courses if student in course.students]
                if student_classes:
                    print("Here is your current schedule")
                    for course in student_classes:
                        print(f"ID: {course.course_id}, Name: {course.name}")
                else:
                    print("You haven't registered for classes yet.")

            elif option == "2":
                print(f"{student.name}'s Grades: ")
                if student.grades:
                    for course_name, grades in student.grades.items():
                        average = sum(grades) / len(grades)
                        print(f"{course_name}: {', '.join(map(str, grades))}")
                else:
                    print("No grades available.")

            elif option =="3":
                gpa = student.calculate_gpa()
                print(f"{student.name}'s GPA: {gpa}")

            elif option == "4":
                course_name = input("Enter the class name to add: ").strip()
                course = next((course for course in self.courses if course.name.lower() == course_name.lower()), None)
                if course is None:
                    print("That class is not taught here.")
                elif student in course.students:
                    print(f"{student.name} is already enrolled in {course.name}.")
                else:
                    course.students.append(student)
                    student.add_class(course)
                    student.grades[course.name] = []

                    with get_conn() as conn:
                        cur = conn.cursor()
                        cur.execute(
                            "INSERT OR IGNORE INTO enrollments (student_id, course_id) VALUES (?, ?);",
                            (student.student_id, course.course_id)
                        )
                        conn.commit()

                    print(f"{course.name} has been added to your schedule!")

            elif option == "5":
                course_name = input("Enter the class name you want to drop: ").strip()
                course = next((course for course in self.courses if course.name.lower() == course_name.lower()), None)
                if course is None or student not in course.students:
                    print(f"{course_name} is not a current class you are taking.")
                else:
                    course.students.remove(student)
                    student.drop_class(course)
                    student.grades.pop(course.name, None)

                    with get_conn() as conn:
                        cur = conn.cursor()
                        cur.execute(
                            "DELETE FROM enrollments WHERE student_id=? AND course_id=?;",
                            (student.student_id, course.course_id)
                        )
                        cur.execute(
                            "DELETE FROM grades WHERE student_id=? AND course_id=?;",
                            (student.student_id, course.course_id)
                        )
                        conn.commit()

                    print(f"{course.name} has been dropped.")
            
            elif option =="6":
                print("Exiting student portal")
                return
            
            else: 
                print("Invalid option.")


if __name__ == "__main__":
    overview = Overview()
    overview.run()



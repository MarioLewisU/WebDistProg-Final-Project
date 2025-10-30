from models.student import Student
from models.course import Course
from models.teacher import Teacher
from models.admin import Admin

class Overview:
    def __init__(self):
    
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

                #had ai preload some data
        self.students[0].add_class(self.courses[0])  # John Cena -> English 101
        self.courses[0].add_student(self.students[0])
        self.students[0].add_class(self.courses[1])  # John Cena -> Math 102
        self.courses[1].add_student(self.students[0])
        self.students[0].add_class(self.courses[2])  # John Cena -> Science 103
        self.courses[2].add_student(self.students[0])
        self.students[0].add_class(self.courses[3])  # John Cena -> History 104
        self.courses[3].add_student(self.students[0])

        self.students[1].add_class(self.courses[0])  # Jon Jones -> English 101
        self.courses[0].add_student(self.students[1])
        self.students[1].add_class(self.courses[1])  # Jon Jones -> Math 102
        self.courses[1].add_student(self.students[1])
        self.students[1].add_class(self.courses[3])  # Jon Jones -> History 104
        self.courses[3].add_student(self.students[1])
        self.students[1].add_class(self.courses[4])  # Jon Jones -> Physical Education
        self.courses[4].add_student(self.students[1])

        self.students[2].add_class(self.courses[0])  # Steve Austin -> English 101
        self.courses[0].add_student(self.students[2])
        self.students[2].add_class(self.courses[2])  # Steve Austin -> Science 103
        self.courses[2].add_student(self.students[2])
        self.students[2].add_class(self.courses[3])  # Steve Austin -> History 104
        self.courses[3].add_student(self.students[2])
        self.students[2].add_class(self.courses[4])  # Steve Austin -> Physical Education
        self.courses[4].add_student(self.students[2])

        self.students[3].add_class(self.courses[0])  # Conor McGregor -> English 101
        self.courses[0].add_student(self.students[3])
        self.students[3].add_class(self.courses[1])  # Conor McGregor -> Math 102
        self.courses[1].add_student(self.students[3])
        self.students[3].add_class(self.courses[2])  # Conor McGregor -> Science 103
        self.courses[2].add_student(self.students[3])
        self.students[3].add_class(self.courses[4])  # Conor McGregor -> Physical Education
        self.courses[4].add_student(self.students[3])

        self.students[4].add_class(self.courses[1])  # Jeff Hardy -> Math 102
        self.courses[1].add_student(self.students[4])
        self.students[4].add_class(self.courses[2])  # Jeff Hardy -> Science 103
        self.courses[2].add_student(self.students[4])
        self.students[4].add_class(self.courses[3])  # Jeff Hardy -> History 104
        self.courses[3].add_student(self.students[4])
        self.students[4].add_class(self.courses[4])  # Jeff Hardy -> Physical Education
        self.courses[4].add_student(self.students[4])

       
    def find_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None
        
    def find_class(self, course_id):
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None
    
    def find_teacher(self, teacher_id):
        for teacher in self.teachers:
            if teacher.teacher_id == teacher_id:
                return teacher
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
                print(f"Student {name} has been added with an ID of {student_id}")

            elif option == "2":
                course_id = len(self.courses) + 1
                name = input("Enter the class you would like to create: ")
                course = Course(course_id, name)
                self.admin.create_class(course_id, name)
                self.courses.append(course)
                print(f"{name} has been created as a class with an ID of {course_id}")

            elif option == "3":
                    
                print("Students:")
                for student in self.students:
                    print(f"ID: {student.student_id}, Name: {student.name}")

                print("Classes:")
                for course in self.courses:
                    print(f"ID: {course.course_id}, Name: {course.name}")

                student_id_input = int(input("Enter the students ID: "))
                course_id_input = int(input("Enter the class ID: "))

                student = self.find_student(student_id_input)
                course = self.find_class(course_id_input)

                if student is not None and course is not None:
                    student.add_class(course)
                    course.add_student(student)
                    print(f"{student.name} has been added to {course.name}")
                else:
                    print("Invalid student or class ID")
                
            elif option == "4":
                print("Students")
                for student in self.students:
                    print(f"ID: {student.student_id} Name: {student.name}")

                print("Classes:")
                for course in self.courses:
                    print(f"ID: {course.course_id}, Name: {course.name}")

                student_id_input = int(input("Enter the students ID: "))
                course_id_input = int(input("Enter the class ID: "))

                student = self.find_student(student_id_input)
                course = self.find_class(course_id_input)

                if student and course:
                    student.drop_class(course)
                    course.remove_student(student)
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

            elif option =="4":
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
                    print(f"{course.name} has been dropped.")
            
            elif option =="6":
                print("Exiting student portal")
                return
            
            else: 
                print("Invalid option.")


if __name__ == "__main__":
    overview = Overview()
    overview.run()



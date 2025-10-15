class Course:
    def __init__(self, course_id, name, teacher = None):
        self.course_id = course_id
        self.name = name
        self.teacher = teacher
        self.students = []
        self.assignments = {}
        

    def add_student(self, student):
        self.students.append(student)

    def remove_student(self, student):
        self.students.remove(student)

    def assign_grade(self, student, grade):
        if student.student_id not in self.assignments:
            self.assignments[student.student_id] = []
        self.assignments[student.student_id].append(grade)
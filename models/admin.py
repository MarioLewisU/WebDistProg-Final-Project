from models.course import Course

class Admin:
    def __init__(self,name):
        self.name = name

    def create_class(self, course_id, name, teacher = None):
        return Course(course_id, name, teacher)
    
    def add_student_to_class(self, student, course):
        course.add_student(student)

    def remove_student_from_class(self, student, course):
        course.remove_student(student)
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
        return self.grades
    
    def calculate_gpa(self):
        total_points = 0
        total_classes = 0

        for grades in self.grades.values():
            if grades:
                average = sum(grades) / len(grades)


                if 97 <= average <= 100:
                    letter = "A+"
                    points = 4.0

                elif 93 <= average <= 97:
                    letter = "A"
                    points = 4.0

                elif 90 <= average <= 93:
                    letter = "A-"
                    points = 3.7

                elif 87 <= average <= 90:
                    letter = "B+"
                    points = 3.3

                elif 83 <= average <= 87:
                    letter = "B"
                    points = 3.0

                elif 80 <= average <= 83:
                    letter = "B-"
                    points = 2.7

                elif 77 <= average <= 80:
                    letter = "C+"
                    points = 2.3
                elif 73 <= average <= 77:
                    letter = "C"
                    points = 2.0

                elif 70 <= average <= 73:
                    letter = "C-"
                    points = 1.7

                elif 67 <= average <= 70:
                    letter = "D+"
                    points = 1.3

                elif 63 <= average <= 67:
                    letter = "D"
                    points = 1.0

                elif 60 <= average <= 63:
                    letter = "D-"
                    points = 0.7

                else:
                    letter = "F"
                    points = 0.0
        
                total_points += points
                total_classes += 1
                
        return round(total_points / total_classes) if total_classes > 0 else 0.0
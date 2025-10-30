from flask import Flask, render_template, request, redirect, url_for
from overview import Overview  # Your backend logic

app = Flask(__name__)
overview = Overview()  # Initialize your school data

# index
@app.route('/')
def index():
    return render_template('index.html')  # Choose Admin, Teacher, or Student

# student select
@app.route('/student_select', methods=['GET', 'POST'])
def student_select():
    if request.method == 'POST':
        student_id = int(request.form.get('student_id'))
        return redirect(url_for('student_dashboard', student_id=student_id))
    return render_template('studentselect.html', students=overview.students)

# student dashboard
@app.route('/student_dashboard/<int:student_id>', methods=['GET', 'POST'])
def student_dashboard(student_id):
    student = overview.find_student(student_id)
    if not student:
        return "Student not found", 404

    # Handle form submission
    if request.method == 'POST':
        if 'add_class' in request.form:
            course_id = int(request.form.get('add_class'))
            course = overview.find_class(course_id)
            if course and student not in course.students:
                student.add_class(course)
                course.add_student(student)
        elif 'drop_class' in request.form:
            course_id = int(request.form.get('drop_class'))
            course = overview.find_class(course_id)
            if course and student in course.students:
                student.drop_class(course)
                course.remove_student(student)
        return redirect(url_for('student_dashboard', student_id=student_id))

    
    student_classes = [course for course in overview.courses if student in course.students]
    available_classes = [course for course in overview.courses if student not in course.students]
    gpa = student.calculate_gpa()

    return render_template('studentdashboard.html', student=student,
                           classes=student_classes, available_classes=available_classes, gpa=gpa)

# teacher select
@app.route('/teacher_select', methods=['GET', 'POST'])
def teacher_select():
    if request.method == 'POST':
        teacher_id = int(request.form.get('teacher_id'))
        return redirect(url_for('teacher_dashboard', teacher_id=teacher_id))
    return render_template('teacherselect.html', teachers=overview.teachers)

# teacher dashboard
@app.route('/teacher_dashboard/<int:teacher_id>', methods=['GET', 'POST'])
def teacher_dashboard(teacher_id):
    teacher = overview.find_teacher(teacher_id)
    if not teacher:
        return "Teacher not found", 404

    
    teacher_classes = [course for course in overview.courses if course.teacher == teacher]

    if request.method == 'POST':
        course_id = int(request.form.get('course_id'))
        student_id = int(request.form.get('student_id'))
        grade = float(request.form.get('grade'))

        course = overview.find_class(course_id)
        student = overview.find_student(student_id)

        if course and student:
            student.grades.setdefault(course.name, [])
            student.grades[course.name].append(grade)

        return redirect(url_for('teacher_dashboard', teacher_id=teacher_id))

    return render_template('teacherdashboard.html', teacher=teacher,
                           classes=teacher_classes)

# admin select
@app.route('/admin_select', methods=['GET', 'POST'])
def admin_select():
    message = ""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'admin123':
            return redirect(url_for('admin_dashboard'))
        else:
            message = "Incorrect password. Please try again."
    return render_template('adminselect.html', message=message)

# admin dashboard
@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    message = ""
    if request.method == 'POST':
        print("Form Data:", request.form)  # Debug print

        try:
            action = request.form.get('action')
            print("Action received:", action)

            if action == "add_student":
                name = request.form.get('student_name')
                student_id = len(overview.students) + 1
                from models.student import Student
                new_student = Student(student_id, name)
                overview.students.append(new_student)
                message = f"Student {name} added and assigned ID {student_id}."

            elif action == "create_class":
                class_name = request.form.get('class_name')
                course_id = len(overview.courses) + 1
                from models.course import Course
                new_course = Course(course_id, class_name)
                overview.courses.append(new_course)
                message = f"Class {class_name} created."

            elif action == "add_student_class":
                student_id = int(request.form.get('student_id'))
                course_id = int(request.form.get('course_id'))
                student = overview.find_student(student_id)
                course = overview.find_class(course_id)
                if student and course:
                    course.students.append(student)
                    student.add_class(course)
                    message = f"{student.name} added to {course.name}."
                else:
                    message = "Student or class not found."

            elif action == "remove_student_class":
                student_id = int(request.form.get('student_id'))
                course_id = int(request.form.get('course_id'))
                student = overview.find_student(student_id)
                course = overview.find_class(course_id)
                if student and course and student in course.students:
                    course.students.remove(student)
                    student.drop_class(course)
                    message = f"{student.name} removed from {course.name}."
                else:
                    message = "Student or class not found."

            elif action == "modify_grade":
                student_id = int(request.form.get('student_id'))
                course_id = int(request.form.get('course_id'))
                grade = float(request.form.get('grade'))
                student = overview.find_student(student_id)
                course = overview.find_class(course_id)
                if student and course:
                    student.grades.setdefault(course.name, []).append(grade)
                    message = f"Added grade {grade} for {student.name} in {course.name}."
                else:
                    message = "Student or class not found."

        except Exception as e:
            message = f"Error: {e}"
            print("Error occurred:", e)

    return render_template('admindashboard.html',
                           students=overview.students,
                           courses=overview.courses,
                           message=message)



if __name__ == '__main__':
    app.run(debug=True)

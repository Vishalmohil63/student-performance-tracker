import database

class StudentTracker:
    def __init__(self):
        database.init_db()

    def add_student(self, roll, name):
        database.add_student(roll, name)

    def list_students(self):
        return database.list_students()

    def add_grade(self, roll, subject, grade):
        database.add_grade(roll, subject, grade)

    def get_student_details(self, roll):
        return database.get_student_details(roll)

    def class_average(self):
        return database.get_class_averages()

    def subject_topper(self):
        return database.get_subject_toppers()

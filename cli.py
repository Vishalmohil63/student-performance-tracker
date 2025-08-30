# cli.py
from models import StudentTracker

tracker = StudentTracker()

def menu():
    print("""
===== Student Performance Tracker =====
1. Add Student
2. Add Grade
3. View Student Details
4. List Students
5. Calculate Student Average
6. Subject Topper
7. Class Average
0. Exit
""")

while True:
    menu()
    choice = input("Enter choice: ").strip()

    if choice == "1":
        name = input("Enter name: ")
        roll = input("Enter roll number: ")
        try:
            tracker.add_student(name, roll)
            print("✅ Student added!")
        except Exception as e:
            print("❌", e)

    elif choice == "2":
        roll = input("Roll number: ")
        subject = input("Subject: ")
        try:
            grade = float(input("Grade (0-100): "))
            tracker.add_grade(roll, subject, grade)
            print("✅ Grade added!")
        except Exception as e:
            print("❌", e)

    elif choice == "3":
        roll = input("Roll number: ")
        details = tracker.get_student_details(roll)
        if not details:
            print("❌ Student not found.")
        else:
            print("Name:", details["name"])
            print("Roll:", details["roll_number"])
            if details["grades"]:
                for subj, grd in details["grades"].items():
                    print(f"  {subj}: {grd}")
            else:
                print("No grades yet.")

    elif choice == "4":
        students = tracker.list_students()
        if not students:
            print("No students found.")
        else:
            for s in students:
                print(s["roll_number"], "-", s["name"])

    elif choice == "5":
        roll = input("Roll number: ")
        avg = tracker.calculate_average(roll)
        if avg is None:
            print("❌ No grades found for this student.")
        else:
            print(f"Average: {avg:.2f}")

    elif choice == "6":
        subject = input("Subject: ")
        topper = tracker.subject_topper(subject)
        if topper:
            print(f"Topper in {subject}: {topper['name']} ({topper['roll_number']}) - {topper['grade']}")
        else:
            print("❌ No data for this subject.")

    elif choice == "7":
        subject = input("Subject: ")
        avg = tracker.class_average(subject)
        if avg is None:
            print("❌ No data for this subject.")
        else:
            print(f"Class average in {subject}: {avg:.2f}")

    elif choice == "0":
        print("Bye!")
        break
    else:
        print("Invalid choice.")
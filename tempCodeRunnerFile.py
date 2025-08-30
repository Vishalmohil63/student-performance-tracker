from flask import Flask, render_template, request, redirect, url_for, flash
import database

app = Flask(__name__)
app.secret_key = "supersecret"

@app.route("/")
def index():
    students = database.list_students()
    stats = {
        "total_students": database.total_students(),
        "total_subjects": database.total_subjects(),
        "total_grades": database.total_grades(),
    }
    return render_template("index.html", students=students, stats=stats)

# ---------- Add Student ----------
@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        roll = request.form.get("roll", "").strip()
        name = request.form.get("name", "").strip()
        try:
            if not roll or not name:
                raise ValueError("Roll number and name are required.")
            database.add_student(roll, name)
            flash("✅ Student added successfully!", "success")
            return redirect(url_for("index"))
        except Exception as e:
            flash(f"❌ {e}", "error")
            return redirect(url_for("add_student"))
    return render_template("add_student.html")

# ---------- Add Grade ----------
@app.route("/add-grade", methods=["GET", "POST"])
def add_grade():
    if request.method == "POST":
        roll = request.form.get("roll", "").strip()
        subject = request.form.get("subject", "").strip()
        grade_raw = request.form.get("grade", "").strip()
        try:
            if not roll or not subject or not grade_raw:
                raise ValueError("All fields are required.")
            grade = int(grade_raw)
            if grade < 0 or grade > 100:
                raise ValueError("Grade must be between 0 and 100.")
            database.add_grade(roll, subject, grade)
            flash("✅ Grade added successfully!", "success")
            return redirect(url_for("index"))
        except Exception as e:
            flash(f"❌ {e}", "error")
            return redirect(url_for("add_grade"))
    return render_template("add_grade.html")

# ---------- View Student ----------
@app.route("/student/<roll>")
def view_student(roll):
    student = database.get_student_by_roll(roll)
    grades = database.get_grades_by_roll(roll)
    if not student:
        flash("❌ Student not found.", "error")
        return redirect(url_for("index"))
    return render_template("view_student.html", student=student, grades=grades)

# ---------- Reports ----------
@app.route("/reports")
def reports():
    report_data = database.get_full_report()
    return render_template("reports.html", report_data=report_data)

# ---------- Subject Toppers ----------
@app.route("/subject-topper")
def subject_topper():
    toppers = database.get_subject_toppers()
    return render_template("subject_topper.html", toppers=toppers)

# ---------- Class Average (Chart) ----------
@app.route("/class-average")
def class_average():
    data = database.get_class_average()
    subjects = [d["subject"] for d in data]
    values = [d["avg_grade"] for d in data]
    totals = [d["total_students"] for d in data]
    return render_template("class_averages_chart.html", subjects=subjects, values=values, totals=totals)

if __name__ == "__main__":
    database.init_db()
    app.run(debug=True)

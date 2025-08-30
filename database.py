import sqlite3
from contextlib import closing

DB_NAME = "student_tracker.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # dict-like rows
    return conn

# ------------------ INIT ------------------
def init_db():
    with closing(get_connection()) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_number TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject TEXT NOT NULL,
                grade INTEGER NOT NULL,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        """)
        conn.commit()

# ------------------ STUDENTS ------------------
def add_student(roll_number, name):
    with closing(get_connection()) as conn:
        conn.execute("INSERT INTO students (roll_number, name) VALUES (?, ?)", (roll_number, name))
        conn.commit()

def list_students():
    with closing(get_connection()) as conn:
        rows = conn.execute("SELECT id, roll_number, name FROM students ORDER BY roll_number").fetchall()
        return [dict(r) for r in rows]

def get_student_by_roll(roll_number):
    with closing(get_connection()) as conn:
        row = conn.execute("SELECT id, roll_number, name FROM students WHERE roll_number = ?", (roll_number,)).fetchone()
        return dict(row) if row else None

# ------------------ GRADES ------------------
def add_grade(roll_number, subject, grade):
    with closing(get_connection()) as conn:
        stu = conn.execute("SELECT id FROM students WHERE roll_number = ?", (roll_number,)).fetchone()
        if not stu:
            raise ValueError("Student not found")
        conn.execute(
            "INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)",
            (stu["id"], subject, grade)
        )
        conn.commit()

def get_grades_by_roll(roll_number):
    with closing(get_connection()) as conn:
        stu = conn.execute("SELECT id FROM students WHERE roll_number = ?", (roll_number,)).fetchone()
        if not stu:
            return []
        rows = conn.execute("SELECT subject, grade FROM grades WHERE student_id = ? ORDER BY subject", (stu["id"],)).fetchall()
        return [dict(r) for r in rows]

# ------------------ ANALYTICS / REPORTS ------------------
def get_full_report():
    with closing(get_connection()) as conn:
        rows = conn.execute("""
            SELECT s.roll_number, s.name, g.subject, g.grade
            FROM students s
            LEFT JOIN grades g ON s.id = g.student_id
            ORDER BY s.roll_number, g.subject
        """).fetchall()
        return [dict(r) for r in rows]

def get_subject_toppers():
    with closing(get_connection()) as conn:
        rows = conn.execute("""
            SELECT g.subject, s.name, s.roll_number, MAX(g.grade) AS max_grade
            FROM grades g
            JOIN students s ON g.student_id = s.id
            GROUP BY g.subject
            ORDER BY g.subject
        """).fetchall()
        return [dict(r) for r in rows]

def get_class_average():
    with closing(get_connection()) as conn:
        rows = conn.execute("""
            SELECT subject, ROUND(AVG(grade), 2) AS avg_grade, COUNT(*) AS total_students
            FROM grades
            GROUP BY subject
            ORDER BY subject
        """).fetchall()
        return [dict(r) for r in rows]

# ------------------ STATS (for dashboard cards) ------------------
def total_students():
    with closing(get_connection()) as conn:
        row = conn.execute("SELECT COUNT(*) AS c FROM students").fetchone()
        return row["c"]

def total_subjects():
    with closing(get_connection()) as conn:
        row = conn.execute("SELECT COUNT(DISTINCT subject) AS c FROM grades").fetchone()
        return row["c"]

def total_grades():
    with closing(get_connection()) as conn:
        row = conn.execute("SELECT COUNT(*) AS c FROM grades").fetchone()
        return row["c"]

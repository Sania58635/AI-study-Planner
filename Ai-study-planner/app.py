import sqlite3

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

DB_NAME = "study_planner.db"


def get_db_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def setup_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            deadline TEXT NOT NULL,
            due_date TEXT NOT NULL,
            progress INTEGER NOT NULL
        )
    """)

    existing_courses = connection.execute("SELECT COUNT(*) FROM courses").fetchone()[0]

    if existing_courses == 0:
        connection.execute("""
            INSERT INTO courses (name, deadline, due_date, progress)
            VALUES (?, ?, ?, ?)
        """, ("Computer Science", "Project proposal", "June 14", 65))

    connection.commit()
    connection.close()


@app.route("/", methods=["GET", "POST"])
def home():
    flashcards = []
    connection = get_db_connection()

    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "assignment":
            course_name = request.form.get("course_name")
            deadline = request.form.get("deadline")
            due_date = request.form.get("due_date")
            progress = request.form.get("progress")

            connection.execute("""
                INSERT INTO courses (name, deadline, due_date, progress)
                VALUES (?, ?, ?, ?)
            """, (course_name, deadline, due_date, int(progress)))

            connection.commit()
            connection.close()

            return redirect("/")

        if form_type == "flashcards":
            notes = request.form.get("notes")

            if notes:
                sentences = [s.strip() for s in notes.split(".") if s.strip()]

                for sentence in sentences[:5]:
                    flashcards.append({
                        "question": f"What is important about: {sentence[:50]}?",
                        "answer": sentence
                    })

    courses = connection.execute("SELECT * FROM courses").fetchall()
    connection.close()

    return render_template("index.html", courses=courses, flashcards=flashcards)


if __name__ == "__main__":
    setup_database()
    app.run(debug=True)
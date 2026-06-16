import sqlite3

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

DB_NAME = "school_calendar.db"


def get_db_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def setup_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            class_name TEXT NOT NULL,
            due_date TEXT NOT NULL,
            priority TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/", methods=["GET", "POST"])
def home():
    connection = get_db_connection()

    if request.method == "POST":
        title = request.form.get("title")
        class_name = request.form.get("class_name")
        due_date = request.form.get("due_date")
        priority = request.form.get("priority")

        connection.execute("""
            INSERT INTO tasks (title, class_name, due_date, priority)
            VALUES (?, ?, ?, ?)
        """, (title, class_name, due_date, priority))

        connection.commit()
        connection.close()

        return redirect("/")

    tasks = connection.execute("""
        SELECT * FROM tasks
        ORDER BY due_date ASC
    """).fetchall()

    connection.close()

    return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    connection = get_db_connection()

    connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    connection.commit()
    connection.close()

    return redirect("/")


if __name__ == "__main__":
    setup_database()
    app.run(debug=True)
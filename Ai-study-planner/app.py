import calendar
import sqlite3
from datetime import date, timedelta

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


def group_tasks_by_date(tasks):
    tasks_by_date = {}

    for task in tasks:
        tasks_by_date.setdefault(task["due_date"], []).append(task)

    return tasks_by_date


def build_month_view(tasks):
    today = date.today()
    weeks = calendar.Calendar(firstweekday=6).monthdatescalendar(today.year, today.month)
    tasks_by_date = group_tasks_by_date(tasks)

    month_weeks = []

    for week in weeks:
        month_week = []

        for day in week:
            day_key = day.isoformat()

            month_week.append({
                "number": day.day,
                "date": day_key,
                "in_month": day.month == today.month,
                "is_today": day == today,
                "tasks": tasks_by_date.get(day_key, [])
            })

        month_weeks.append(month_week)

    return today.strftime("%B %Y"), month_weeks


def build_week_view(tasks):
    today = date.today()
    start_of_week = today - timedelta(days=(today.weekday() + 1) % 7)
    tasks_by_date = group_tasks_by_date(tasks)

    week_days = []

    for i in range(7):
        day = start_of_week + timedelta(days=i)
        day_key = day.isoformat()

        week_days.append({
            "name": day.strftime("%A"),
            "number": day.day,
            "date": day_key,
            "is_today": day == today,
            "tasks": tasks_by_date.get(day_key, [])
        })

    end_of_week = start_of_week + timedelta(days=6)
    week_title = f"{start_of_week.strftime('%b %d')} - {end_of_week.strftime('%b %d, %Y')}"

    return week_title, week_days


def build_year_view(tasks):
    today = date.today()
    months = []

    for month in range(1, 13):
        month_tasks = []

        for task in tasks:
            task_date = date.fromisoformat(task["due_date"])

            if task_date.year == today.year and task_date.month == month:
                month_tasks.append(task)

        months.append({
            "name": calendar.month_name[month],
            "task_count": len(month_tasks),
            "tasks": month_tasks[:4]
        })

    return str(today.year), months


@app.route("/", methods=["GET", "POST"])
def home():
    setup_database()
    connection = get_db_connection()

    if request.method == "POST":
        title = request.form.get("title")
        class_name = request.form.get("class_name")
        due_date = request.form.get("due_date")
        priority = request.form.get("priority")

        if title and class_name and due_date and priority:
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

    month_name, calendar_weeks = build_month_view(tasks)
    week_title, week_days = build_week_view(tasks)
    year_title, year_months = build_year_view(tasks)

    connection.close()

    return render_template(
        "index.html",
        tasks=tasks,
        month_name=month_name,
        calendar_weeks=calendar_weeks,
        week_title=week_title,
        week_days=week_days,
        year_title=year_title,
        year_months=year_months
    )


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
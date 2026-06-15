from flask import Flask, render_template, request, redirect

app = Flask(__name__)

courses = [
    {
        "name": "Computer Science",
        "deadline": "Project proposal",
        "due_date": "June 14",
        "progress": 65,
    }
]

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        course_name = request.form.get("course_name")
        deadline = request.form.get("deadline")
        due_date = request.form.get("due_date")
        progress = request.form.get("progress")

        new_course = {
            "name": course_name,
            "deadline": deadline,
            "due_date": due_date,
            "progress": int(progress),
        }

        courses.append(new_course)

        return redirect("/")

    return render_template("index.html", courses=courses, flashcards=[])

if __name__ == "__main__":
    app.run(debug=True)
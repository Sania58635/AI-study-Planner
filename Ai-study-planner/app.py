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
    flashcards = []

    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "assignment":
            new_course = {
                "name": request.form.get("course_name"),
                "deadline": request.form.get("deadline"),
                "due_date": request.form.get("due_date"),
                "progress": int(request.form.get("progress")),
            }

            courses.append(new_course)
            return render_template("index.html", courses=courses, flashcards=flashcards)

        if form_type == "flashcards":
            notes = request.form.get("notes")

            if notes:
                sentences = [s.strip() for s in notes.split(".") if s.strip()]

                for sentence in sentences[:5]:
                    flashcards.append({
                        "question": f"What is important about: {sentence[:50]}?",
                        "answer": sentence
                    })

    return render_template("index.html", courses=courses, flashcards=flashcards)

if __name__ == "__main__":
    app.run(debug=True)
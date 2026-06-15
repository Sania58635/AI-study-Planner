from flask import Flask, render_template, request

app = Flask(__name__)

courses = [
    {
        "name": "Computer Science",
        "deadline": "Project proposal",
        "due_date": "June 14",
        "progress": 65,
    },
    {
        "name": "Calculus",
        "deadline": "Homework 5",
        "due_date": "June 12",
        "progress": 40,
    },
    {
        "name": "English",
        "deadline": "Essay draft",
        "due_date": "June 18",
        "progress": 80,
    },
]

@app.route("/", methods=["GET", "POST"])
def home():
    flashcards = []

    if request.method == "POST":
        notes = request.form.get("notes", "")
        sentences = [s.strip() for s in notes.split(".") if s.strip()]

        for sentence in sentences[:5]:
            flashcards.append({
                "question": f"What is important about: {sentence[:50]}?",
                "answer": sentence
            })

    return render_template("index.html", courses=courses, flashcards=flashcards)

if __name__ == "__main__":
    app.run(debug=True)
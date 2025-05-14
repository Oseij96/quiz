from flask import Flask, render_template, request, redirect, session, url_for
import json, random

app = Flask(__name__)


def load_questions():
    with open('questions.json') as f:
        data = json.load(f)
        random.shuffle(data)
        return data

@app.route("/", methods=["GET", "POST"])
def quiz():
    if 'questions' not in session:
        session['questions'] = load_questions()
        session['current'] = 0
        session['score'] = 0

    questions = session['questions']
    index = session['current']

    # Check if the current index exceeds the total number of questions
    if index >= len(questions):
        return redirect(url_for('result'))

    if request.method == "POST":
        user_answer = request.form.get('answer', '').strip().lower()
        correct_answer = questions[index]['answer'].strip().lower()

        if user_answer == correct_answer:
            session['score'] += 1

        session['current'] += 1

        # Redirect to the quiz page after answering
        return redirect(url_for('quiz'))

    # Render the current question
    question = questions[index]
    return render_template("quiz.html", question=question)


@app.route("/result")
def result():
    score = session.get('score', 0)
    total = len(session.get('questions', []))
    return render_template("result.html", score=score, total=total)


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for('quiz'))


if __name__ == "__main__":
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()

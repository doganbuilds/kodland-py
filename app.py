from flask import (
    Flask,
    make_response,
    redirect,
    render_template,
    request,
    flash,
    url_for,
)
from werkzeug import Response
import werkzeug
import werkzeug.exceptions
from database import db_session, init_db
from models import Question, Score
from utils.get_answer import get_answer_from_question, get_user_answer

app = Flask(__name__)
app.secret_key = "ajh(hro^840^(+Ujnn))"


@app.errorhandler(werkzeug.exceptions.MethodNotAllowed)
def handle_method_not_allowed(e):
    return redirect(url_for("index_route"))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


init_db()


@app.route("/")
def index_route() -> Response:
    resp = make_response(render_template("index.template.html"))

    if request.cookies.get("name") and request.cookies.get("surname"):
        user = request.cookies.get("name") + " " + request.cookies.get("surname")  # type: ignore
        best_score = Score.query.filter_by(name=user).order_by(Score.score.desc()).first()  # type: ignore
        resp.set_cookie("score", str(best_score.score) if best_score else "")

    return resp


@app.route("/quiz", methods=["POST"])
def quiz_route() -> str | Response:
    name = request.form.get("name")
    surname = request.form.get("surname")

    if name == None or name == "" or surname == None or surname == "":
        if name == None or name == "":
            flash("İsim alanı boş bırakılamaz.", "error")

        if surname == None or surname == "":
            flash("Soyisim alanı boş bırakılamaz.", "error")

        return redirect(url_for("index_route"))

    questions = Question.query.all()

    response = make_response(render_template("quiz.template.html", questions=questions))
    response.set_cookie("name", name)
    response.set_cookie("surname", surname)
    return response


@app.route("/answer", methods=["POST"])
def answer_route():
    questions = Question.query.all()
    q = []
    for question in questions:
        correct_answer = get_answer_from_question(question)
        user_answer = get_user_answer(
            question, request.form.get("question" + str(question.id))
        )

        if request.form.get("question" + str(question.id)) == question.answer:
            q.append(
                {
                    "question": question.question,
                    "result": True,
                    "answer": correct_answer,
                    "user_answer": user_answer,
                }
            )
        else:
            q.append(
                {
                    "question": question.question,
                    "result": False,
                    "answer": correct_answer,
                    "user_answer": user_answer,
                }
            )

    correct = len([x for x in q if x["result"] == True])
    wrong = len([x for x in q if x["result"] == False])
    percentage = (correct / len(questions)) * 100

    results = {
        "results": q,
        "total": len(questions),
        "correct": correct,
        "wrong": wrong,
        "percentage": percentage,
    }

    score = Score(
        name=request.cookies.get("name") + " " + request.cookies.get("surname"),  # type: ignore
        score=percentage,
    )
    db_session.add(score)
    db_session.commit()

    return render_template(
        "result.template.html",
        results=results,
        name=request.cookies.get("name"),
        surname=request.cookies.get("surname"),
    )


@app.route("/leaderboard")
def leaderboard_route():
    leaderboard = db_session.query(Score).distinct(Score.name).order_by(Score.score.desc()).all()  # type: ignore
    return render_template("leaderboard.template.html", leaderboard=leaderboard)


@app.route("/init")
def init_route():
    q1 = Question(
        question="Yapay Zeka (AI) Ne Yapar?",
        option1="Bilgisayarların insan gibi düşünmesini sağlar",
        option2="Yeni yemek tarifleri bulur",
        option3="Evde temizlik yapar",
        option4="Video oyunları oynar",
        answer="option1",
    )

    q2 = Question(
        question="Bir robot, yapay zekayı kullanarak ne yapabilir?",
        option1="Matematik problemi çözebilir",
        option2="Resim yapabilir",
        option3="Müzik besteleyebilir",
        option4="Hepsi",
        answer="option4",
    )

    q3 = Question(
        question="TensorFlow Nedir?",
        option1="Bir oyun",
        option2="Bir yapay zeka aracı",
        option3="Bir spor ekipmanı",
        option4="Bir yemek tarifi",
        answer="option2",
    )

    q4 = Question(
        question="TensorFlow ile hangi tür projeler yapılabilir?",
        option1="Yüz tanıma",
        option2="Sesli asistanlar (örneğin Siri)",
        option3="Resim tanıma",
        option4="Hepsi",
        answer="option4",
    )

    db_session.add(q1)
    db_session.add(q2)
    db_session.add(q3)
    db_session.add(q4)

    db_session.commit()
    return "Database initialized"


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, render_template, redirect, flash, jsonify, url_for, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "chimuelo321"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/')
def home():
    
    return render_template('home.html', survey=survey)


@app.route("/begin", methods =['POST'])
def start_survey():

    session[RESPONSES_KEY] = []
    return redirect("/questions/0")
    

@app.route('/questions/<int:question_num>')
def question(question_num):

    responses = session.get(RESPONSES_KEY)

    if(responses is None):
        return redirect("/")

    expected_question_num = len(responses)

    if(expected_question_num == len(survey.questions)):

        return redirect("/complete")

    if (expected_question_num != question_num):
        # Trying to access questions out of order.
        flash(f"Invalid access. You have been redirect to your current question.", "error")
        return redirect(f"/questions/{expected_question_num}")

    question = survey.questions[question_num]
    return render_template("question.html", question_num=question_num, question=question)


@app.route('/answer', methods=['POST'])
def answer_question():
    user_answer = request.form['choice']

    responses= session[RESPONSES_KEY]
    responses.append(user_answer)
    session[RESPONSES_KEY] = responses

    next_question_num = len(responses)

    if (next_question_num == len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{next_question_num}")


@app.route('/complete')
def survey_complete():
    return render_template('complete.html', responses=session[RESPONSES_KEY], survey=survey)
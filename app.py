from flask import Flask, request, render_template, redirect, flash, jsonify, url_for, abort, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey, personality_quiz, surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = "chimuelo321"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)

responses = []
survey=satisfaction_survey

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/', methods =['GET', 'POST'])
def home():
    if request.method == 'POST':
        session['responses'] = []
        return redirect(url_for('question', question_num=0))
    
    return render_template("home.html", survey=survey)

@app.route('/questions/<int:question_num>', methods=['GET', 'POST'])
def question(question_num):
    if question_num >= len(survey.questions) or question_num < len(responses):
        # If the question number is out of range or has already been answered,
        # redirect them to the appropriate question or the thank you page.
        next_question_num = len(responses) if question_num >= len(survey.questions) else question_num + 1
        flash('You attempted to access an invalid question. Redirected to the next available question.')
        return redirect(url_for('question', question_num=next_question_num))

    expected_question_num = len(responses)
    if question_num != expected_question_num:
        # If the user manually types a higher question number, redirect them to the next expected question.
        flash('You attempted to access an invalid question. Redirected to the next expected question.')
        return redirect(url_for('question', question_num=expected_question_num))

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        responses.append(user_answer)

        if expected_question_num + 1 < len(survey.questions):
           return redirect(url_for('question', question_num=expected_question_num + 1))
        else:
          return redirect(url_for('survey_complete'))

    current_question = survey.questions[expected_question_num]
    return render_template('question.html', question=current_question, question_num=expected_question_num)



@app.route('/answer', methods=['POST'])
def answer():
    user_answer = request.form['choice']

    responses.append(user_answer)

    next_question_num = len(responses)

    if next_question_num < len(satisfaction_survey.questions):
        return redirect(url_for('question', question_num=next_question_num))
    else:
        return redirect(url_for('survey_complete'))

@app.route('/complete')
def survey_complete():
    return render_template('complete.html', responses=responses, survey=survey)
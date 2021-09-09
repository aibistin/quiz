# app/main/routes.py
from datetime import datetime
# HTML template module
from flask import flash, redirect, render_template, request, session, url_for
from flask import g, jsonify
from app import current_app, db
from app.main import bp
from app.models import User, Question, Option, UserQuestion, token_required


@bp.route("/", methods=['GET', 'POST'])
@token_required
def home():
    current_app.logger.error(
        "[home] No reson to get here except to redirect to registration")


@bp.route('/test/<user_token>', methods=['GET', 'POST'])
@token_required
def test(current_user=None):

    current_app.logger.debug("Got to test route")
    last_answered_id = current_user.last_answered_question_id()

    if request.method == 'POST':
        current_app.logger.debug("POST request")
        answer_data = request.get_json() or {}
        answered_question_id = answer_data["QuestionId"]
        last_unanswered_question_id = current_user.get_last_unanswered_question_id()

        if int(answered_question_id) != int(last_unanswered_question_id):
            current_app.logger.error("You answered the wrong question!")
            current_app.logger.error("Got answered id:" + answered_question_id)
            current_app.logger.error(
                "Expected Id:" + str(last_unanswered_question_id))
        else:
            current_app.logger.debug("Saving your answer")
            current_user.save_the_answer_to_db(answer_data)

    data = {}
    next_question = current_user.get_next_question()
    if next_question:
        current_app.logger.debug("Saving your Question")
        current_user.save_the_question_to_db(next_question.id)
        current_app.logger.debug("Next Question Id: " + str(next_question.id))
        data["current_question"] = next_question.to_dict()
    else:
        current_app.logger.error("ERROR! No more questions")
        #TODO Tally answers, final survey, finish

    data['next_url'] = url_for('main.test', user_token=current_user.get_quoted_token(),
                               next_question_id=next_question.id if next_question else None)
    data['prev_url'] = url_for('main.test', user_token=current_user.get_quoted_token(),
                               previous_question_id=last_answered_id)
    data["user"] = current_user.to_dict()

    return jsonify(data)

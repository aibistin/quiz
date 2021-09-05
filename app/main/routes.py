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
    current_app.logger.error("[home] No reson to get here")
    current_app.logger.debug("[home] Session: ")
    current_app.logger.debug(session)
    current_app.logger.debug("------ End Session ----")
    current_app.logger.debug("[home] Args: ")
    stuff = request.args
    current_app.logger.debug(stuff)
    current_app.logger.debug("[home] ------ End Args ----")


@bp.route('/test/<user_token>', methods=['GET', 'POST'])
@token_required
def test(current_user=None):

    current_app.logger.debug("Got to test route")
    # all_question_ids = (db.session.query(Question.id).order_by(Question.id)).all()[0:2]

    next_question = last_answered = None
    last_answered_id = next_question_id = 0
    answered_already = (current_user.answered_questions()).all() or []
    current_app.logger.debug("Answered Already")
    if len(answered_already):
        last_answered = answered_already[-1]
        current_app.logger.debug(last_answered)
        last_answered_id = last_answered.question_id
        next_question = (db.session.query(Question).filter(
            Question.id > last_answered.question_id).order_by(Question.id)).first()
    else:
        next_question = (db.session.query(
            Question).order_by(Question.id)).first()

    current_app.logger.debug("Next Question")
    current_app.logger.debug(next_question)
    next_question_id = next_question.id

    # current_question_id = all_question_ids[0]
    # current_app.logger.debug("Current Q Id: " + str(current_question_id))
    # next_question_id = all_question_ids[1]
    # current_app.logger.debug("Next Q Id: " + str(next_question_id))
    # current_app.logger.debug("[test_route] Session: ")
    # current_app.logger.debug(session)
    # current_app.logger.debug("[test_route] ------ End Session ----")

    data = {}

    if request.method == 'POST':
        answer_data = request.get_json() or {}
        answered_question_id = answer_data["QuestionId"]
        ####
        current_app.logger.debug("[test_route] Post Ans: ")
        current_app.logger.debug(answer_data)
        current_app.logger.debug("[test_route] ------ End POST ----")

        if int(answered_question_id) != int(next_question_id):
            current_app.logger.error("You answered the wrong question!")
            current_app.logger.error("Answered Id:" + answered_question_id)
            current_app.logger.error(
                "Expected Answered Id:" + str(next_question_id))
        else:
            current_user.save_the_answer(answer_data)

        page = request.args.get('page', 1, type=int)
        answered_already = (current_user.answered_questions()).all()
        if len(answered_already):
            last_answered = answered_already[-1] 
            next_question = (db.session.query(Question).filter( Question.id > last_answered.question_id).order_by(Question.id)).first()
            last_answered_id = last_answered.question_id
    else:
        page = request.args.get('page', 1, type=int)
        current_app.logger.debug("Last answered id: " + str(last_answered_id))
        next_question = (db.session.query(Question).filter(
            Question.id > last_answered_id).order_by(Question.id)).first()

    data["current_question"] = next_question.to_dict()
    current_app.logger.debug("[test_route] Current page: " + str(page))
    # data = Question.to_collection_dict(Question.query, page, 1, 'main.home')
    # current_app.logger.error('[test_route] All Question Data: ' + str(data))

    asked_questions = ([question.to_dict()
                        for question in current_user.questions.all()])
    current_app.logger.debug(
        "[test_route] Asked questions for " + current_user.username())
    current_app.logger.debug(asked_questions)
    current_app.logger.debug("[test_route] Next Question")
    current_app.logger.debug(data["current_question"])

    data['next_url'] = url_for('main.test', user_token=current_user.get_quoted_token(),
                               next_question_id=next_question.id) if next_question else None
    # data['next_url'] = url_for('main.test', user_token=current_user.get_quoted_token(),
    data['prev_url'] = url_for('main.test', user_token=current_user.get_quoted_token(),
                               previous_question_id=last_answered_id)
    # return jsonify({**current_question, **{'next_url' : next_url ,'prev_url': prev_url }})
    data["user"] = current_user.to_dict()

    per_page = request.args

    return jsonify(data)

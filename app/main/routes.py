# app/main/routes.py
from datetime import datetime
# HTML template module
from flask import flash, redirect, render_template, request, session, url_for
from flask import g, jsonify
from app import current_app, db
from app.main import bp
from app.models import User, Question, Option, token_required


@bp.route("/", methods=['GET', 'POST'])
@bp.route("/test", methods=['GET', 'POST'])
@token_required
def home():

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
    if current_user:
        current_app.logger.debug("[test_route] You are logged in as: ")
        current_app.logger.debug(current_user)

    current_app.logger.debug("[test_route] Session: ")
    current_app.logger.debug(session)
    current_app.logger.debug("[test_route] ------ End Session ----")
    current_app.logger.debug("[test_route] Args: ")
    stuff = request.args
    current_app.logger.debug(stuff)
    current_app.logger.debug("[test_route] ------ End Args ----")

    # if request.method == 'POST'
    # if request.method == 'GET'
    if request.method == 'POST':
        answer = request.get_json() or {}
        # answer = request.json
        current_app.logger.debug("[test_route] Post Ans: ")
        current_app.logger.debug(answer)
        current_app.logger.debug("[test_route] ------ End POST ----")

       #  g.current_user db.session.add( post) db.session.commit()

    # AnsweredText	null
    # ChildQuestionAnsweredText	null
    # ChildQuestionAnsweredText2	null
    # OptionId	"11427870"
    # QuestionId	2474351

    # print(current_app.config)
    # if form.validate_on_submit():
    # msg = Question(body=form.question.data, sender=current_user)
    # db.session.add(msg)
    # db.session.commit()
    # flash("You sent a question!")
    # return redirect(url_for('main.home'))

    page = request.args.get('page', 1, type=int)
    current_app.logger.debug("[test_route] Current page: " + str(page))
    questions = Question.query.order_by(Question.id).paginate(page, 1, False)
    current_question = questions.items[0].to_dict()

    data = Question.to_collection_dict(Question.query, page, 1, 'main.home')
    current_app.logger.error('[test_route] Get Question Data: ' + str(data))

    asked_questions = ([question.to_dict()
                        for question in current_user.asked.all()])
    current_app.logger.debug("[test_route] User Questions for " +
                             current_user.first_name + ' ' + current_user.last_name)
    current_app.logger.debug(asked_questions)
    current_app.logger.debug("[test_route] Current Question")
    current_app.logger.debug(current_question)

    data['next_url'] = url_for('main.test', user_token=current_user.token,
                               page=questions.next_num) if questions.has_next else None
    data['prev_url'] = url_for('main.test', user_token=current_user.token,
                               page=questions.prev_num) if questions.has_prev else None
    # return jsonify({**current_question, **{'next_url' : next_url ,'prev_url': prev_url }})
    data["user"] = current_user.to_dict()

    per_page = request.args

    return jsonify(data)


# ------------------------------------------------------------------------------
#    Answer and Unanswer
# ------------------------------------------------------------------------------

@bp.route('/answer/<username>', methods=['POST'])
@token_required
def answer(username):
    form = EmptyForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash("User, {1} doesn't exist!".format(username))
            return redirect(url_for('main.home'))
        if user == current_user:
            flash("You cannot answer yourself!")
            return redirect(url_for('main.user', username=username))

        current_user.answer(user)
        db.session.commit()
        flash("You are now answer {}!".format(user.username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.home'))

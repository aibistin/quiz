# app/auth/routes.py
from flask import current_app, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.security import safe_str_cmp
from app import db
from app.auth import bp
from app.auth.forms import RegistrationForm
from app.errors import bad_request, error_response
from app.models import User
from datetime import datetime, timedelta

# ------------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------------


@bp.route('/register', methods=["GET", "POST"])
def register():

    if request.method == 'POST':
        data = request.get_json() or {}
        user = None
        if 'csrf_token' not in data:
            current_app.logger.warn("[register] csrf_token not present")
        if 'first_name' not in data or 'last_name' not in data or 'email' not in data:
            return bad_request('Must send first_name, last_name and email fields as a POST request')

        #TODO Add validation
        if User.query.filter_by(email=data['email']).first():
            current_app.logger.warn("[register] Existing User: " + data["email"])
            #TODO Check first_name, last_name also match
            user = User.query.filter_by(email=data["email"]).first()
            if not User.verify_user_token(user.token):
                return bad_request("This candidate's session has ended")
        else:
            current_app.logger.debug("Adding a new user " + data["email"])
            user = User()
            user.from_dict(data, new_user=True)
            db.session.add(user)
            db.session.commit()

        response_data = user.to_dict()
        response_data["next_url"] = url_for('main.test', user_token=user.token)
        response = jsonify(response_data)
        response.status_code = 201
        response.headers['Location'] = url_for('main.test', user_token=user.token)
        return response

    return error_response(401, "Send a POST request with values for, 'first_name', 'last_name' and 'email' ")


@bp.route('/logout')
def logout():

    current_app.logger.warn( "[logout] ")
    if not current_user:
        return bad_request("No user to log out!")

    current_app.logger.warn("Log out user: ")
    current_app.logger.warn(current_user)
    current_user.remove_user_token()

    return redirect(url_for('main.home'))

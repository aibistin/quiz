# app/auth/routes.py
from flask import current_app, jsonify, request, url_for
from app import db
from app.auth import bp
from app.errors import bad_request, error_response
from app.models import User

# ------------------------------------------------------------------------------
#    User Registration
# ------------------------------------------------------------------------------


@bp.route('/register', methods=["GET", "POST"])
def register():

    notify_msg = "Send a POST request with values for, 'first_name', 'last_name' and 'email' "
    if request.method == 'POST':
        data = request.get_json() or {}
        user = None
        if 'first_name' not in data or 'last_name' not in data or 'email' not in data:
            return bad_request(notify_msg)

        # TODO Add input validation
        if User.query.filter_by(email=data['email']).first():
            current_app.logger.warn(
                "[register] Existing User: " + data["email"])
            # TODO Check first_name, last_name also match
            user = User.query.filter_by(email=data["email"]).first()
            if not User.verify_user_token(user.token):
                return bad_request("This candidate's session has ended")
        else:
            current_app.logger.debug("Adding a new user " + data["email"])
            user = User()
            user.from_dict(data)
            db.session.add(user)
            db.session.commit()

        response_data = user.to_dict()

        response_data['test_url'] = request.host_url.rstrip(
            '/') + url_for('main.test', user_token=user.get_token())

        response = jsonify(response_data)
        response.status_code = 201

        response.headers['Location'] = url_for(
            'main.test', user_token=user.token)
        current_app.logger.debug("[register] response data: ")
        current_app.logger.debug(response_data)
        return response

    return error_response(401, notify_msg)

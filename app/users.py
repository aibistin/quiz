# app/api/users.py
from flask import jsonify, request, url_for
from flask_login import login_required
from app import current_app, db
from app.models import User
from app.api import bp
from app.errors import bad_request


@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@login_required
@bp.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    current_app.logger.error('Get Users Data: ' + str(data))
    return jsonify(data)


@bp.route('/users/<int:id>/answers', methods=['GET'])
def get_answers(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.answers, page, per_page,
                                   'api.get_answers', id=id)
    return jsonify(data)


@bp.route('/users/<int:id>/answered', methods=['GET'])
def get_answered(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.answered, page, per_page,
                                   'api.get_answered', id=id)
    return jsonify(data)


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'first_name' not in data or 'last_name' not in data or 'email' not in data:
        return bad_request('Must include first_name, last_name and email fields')
    # if User.query.filter_by(username=data['first_name']).first():
        # return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('Please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    # if 'first_name' in data and 'last_name' in data and \
    #     data['first_name'] != user.first_name and data['last_name'] != user.last_name and \
    #         User.query.filter_by(first_name=data['first_name'] and last_name=data['last_name']).first():
    #     return bad_request('please use a different first and last name combination')

    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())

from flask import jsonify, request, abort, make_response, current_app
from sqlalchemy.exc import IntegrityError

from ..models import User, db
from . import api


# signal definition
def log_request(sender, user, **extra):
    if request.method == 'POST':
        message = 'user is created: id {}'.format(user.id)
    elif request.method == 'PUT':
        message = 'user is updated: id {}'.format(user.id)
    else:
        message = 'user is deleted: id {}'.format(user.id)
    sender.logger.info(message)

# custom 404 error handler
@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'detail': 'Not found'}), 404)


# custom 400 error handler
@api.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'detail': 'Bad request'}), 400)


@api.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify(users=[i.serialize() for i in users])


@api.route('/users', methods=['POST'])
def create_user():
    try:
        new_user = User(
            name=request.json.get('name'),
            description=request.json.get('description'))
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(name=request.json.get('name')).first()
        # signal using
        log_request(current_app._get_current_object(), user)
        return jsonify(user=user.serialize()), 201
    except IntegrityError:
        return abort(400)


@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    id = request.view_args.get('id')
    user = User.query.get_or_404(id)
    return jsonify(user=[user.serialize()])


@api.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        id = request.view_args.get('id')
        user = User.query.get_or_404(id)
        user.name = request.json.get('name')
        user.description = request.json.get('description')
        db.session.commit()
        updated_user = User.query.filter_by(name=user.name).first()
        # signal using
        log_request(current_app._get_current_object(), user)
        return jsonify(user=updated_user.serialize())
    except IntegrityError:
        return abort(400)


@api.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    id = request.view_args.get('id')
    user = User.query.get_or_404(id)
    User.query.filter_by(id=id).delete()
    # signal using
    log_request(current_app._get_current_object(), user)
    db.session.commit()
    return jsonify({}), 204

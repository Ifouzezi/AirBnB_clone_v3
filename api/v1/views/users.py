#!/usr/bin/python3
"""users.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Get user information for all users"""
    users_list = []
    for user in storage.all("User").values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Get user information for a specified user"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a user based on its user_id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Create a new user"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    req_data = request.get_json()
    if 'email' not in req_data:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in req_data:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    user = User(**req_data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Update a user"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    req_data = request.get_json()
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for attr, val in req_data.items():
        if attr not in ignore_keys:
            setattr(user, attr, val)
    user.save()
    return jsonify(user.to_dict())

#!/usr/bin/python3
'''Contains the states view for the API.'''
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    state_objs = storage.all(State)
    return jsonify([state_obj.to_dict() for state_obj in state_objs.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_single_state(state_id):
    """Retrieves a State object"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    return jsonify(state_obj.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    state_obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Returns the new State with the status code 201"""
    new_state_data = request.get_json()
    if not new_state_data:
        abort(400, "Not a JSON")
    if 'name' not in new_state_data:
        abort(400, "Missing name")
    state_obj = State(**new_state_data)
    storage.new(state_obj)
    storage.save()
    return make_response(jsonify(state_obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)

    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")

    for key, value in req_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state_obj, key, value)

    storage.save()
    return make_response(jsonify(state_obj.to_dict()), 200)

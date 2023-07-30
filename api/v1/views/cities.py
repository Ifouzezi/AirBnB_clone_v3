#!/usr/bin/python3
'''Contains the cities view for the API.'''
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieves the list of all City objects of a State"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    return jsonify([city.to_dict() for city in state_obj.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_single_city(city_id):
    """Retrieves a City object"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Returns an empty dictionary with the status code 200"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    city_obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Returns the new City with the status code 201"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)

    new_city_data = request.get_json()
    if not new_city_data:
        abort(400, "Not a JSON")
    if 'name' not in new_city_data:
        abort(400, "Missing name")

    city_obj = City(**new_city_data)
    setattr(city_obj, 'state_id', state_id)
    storage.new(city_obj)
    storage.save()
    return make_response(jsonify(city_obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Returns the City object with the status code 200"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)

    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")

    for key, value in req_data.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city_obj, key, value)

    storage.save()
    return make_response(jsonify(city_obj.to_dict()), 200)

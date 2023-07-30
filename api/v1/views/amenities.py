#!/usr/bin/python3
'''Contains the amenities view for the API.'''
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenity_objs = storage.all(Amenity)
    return jsonify([amenity_obj.to_dict() for amenity_obj in amenity_objs.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_single_amenity(amenity_id):
    """Retrieves a Amenity object"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    return jsonify(amenity_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)

    amenity_obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new Amenity"""
    new_amenity_data = request.get_json()
    if not new_amenity_data:
        abort(400, "Not a JSON")
    if 'name' not in new_amenity_data:
        abort(400, "Missing name")

    amenity_obj = Amenity(**new_amenity_data)
    storage.new(amenity_obj)
    storage.save()
    return make_response(jsonify(amenity_obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity object"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)

    req_data = request.get_json()
    if not req_data:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in req_data.items():
        if key not in ignore_keys:
            setattr(amenity_obj, key, value)

    storage.save()
    return make_response(jsonify(amenity_obj.to_dict()), 200)

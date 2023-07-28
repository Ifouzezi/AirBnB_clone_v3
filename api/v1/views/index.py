#!/usr/bin/python3
"""app.py to connect to API"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage

MODEL_ENDPOINTS = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}

app = Flask(__name__)
app.register_blueprint(app_views)


@app_views.route('/status', strict_slashes=False)
def hbnb_status():
    """Route to return status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def hbnb_stats():
    """Route to return stats"""
    return_dict = {}
    for endpoint, model_name in MODEL_ENDPOINTS.items():
        return_dict[endpoint] = storage.count(model_name)
    return jsonify(return_dict)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

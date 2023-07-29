#!/usr/bin/python3
"""index.py to connect to API"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage

resource_names = {
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
    """hbnbStatus"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def hbnb_stats():
    """hbnbStats"""
    return_dict = {}
    for key, value in resource_names.items():
        return_dict[key] = storage.count(value)
    return jsonify(return_dict)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)

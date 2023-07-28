#!/usr/bin/python3
"""Initialize Blueprint views"""
from flask import Blueprint

# Create a Blueprint named "app_views" with the URL prefix "/api/v1"
api_v1_blueprint = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import view modules from different endpoints
from api.v1.views.index import index_view
from api.v1.views.amenities import amenities_view
from api.v1.views.cities import cities_view
from api.v1.views.places import places_view
from api.v1.views.places_amenities import places_amenities_view
from api.v1.views.places_reviews import places_reviews_view
from api.v1.views.states import states_view
from api.v1.views.users import users_view

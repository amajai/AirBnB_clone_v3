#!/usr/bin/python3
"""Places objects API"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def places(city_id):
    """Get a model object or list of objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", methods=["GET"])
def places_id(place_id):
    """Get a Place object"""
    res = storage.get(Place, place_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def place_delete(place_id):
    """delete model object"""
    res = storage.get(Place, place_id)
    if res is None:
        abort(404)
    storage.delete(res)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """create a new Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    obj = request.get_json(force=True, silent=True)
    if not obj:
        abort(400, "Not a JSON")
    user_id = obj.get("user_id")
    if user_id is None:
        abort(400, "Missing user_id")
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if "name" not in obj:
        abort(400, "Missing name")
    new_place = Place(city_id=city.id, **obj)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """update place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    place.name = data.get("name", place.name)
    place.description = data.get("description", place.description)
    place.number_rooms = data.get("number_rooms", place.number_rooms)
    place.number_bathrooms = data.get("number_bathrooms", place.number_bathrooms)
    place.max_guest = data.get("max_guest", place.max_guest)
    place.price_by_night = data.get("price_by_night", place.price_by_night)
    place.latitude = data.get("latitude", place.latitude)
    place.longitude = data.get("longitude", place.longitude)
    place.save()
    return jsonify(place.to_dict()), 200

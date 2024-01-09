#!/usr/bin/python3
"""Cities objects API"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def cities(state_id):
    """Get a model object or list of objects"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", methods=["GET"])
def cities_id(city_id):
    """Get a City object"""
    res = storage.get(City, city_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def city_delete(city_id):
    """delete model object"""
    res = storage.get(City, city_id)
    if res is None:
        abort(404)
    storage.delete(res)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """create a new city object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    obj = request.get_json(force=True, silent=True)
    if not obj:
        abort(400, "Not a JSON")
    if "name" not in obj:
        abort(400, "Missing name")
    new_city = City(state_id=state.id, **obj)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """update city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    city.name = data.get("name", city.name)
    city.save()
    return jsonify(city.to_dict()), 200

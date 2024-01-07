#!/usr/bin/python3
"""State objects API"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, request, jsonify


@app_views.route("/states", methods=["GET"])
@app_views.route("/states/<state_id>", methods=["GET"])
def states(state_id=None):
    """get a model object or list of objects"""
    if state_id:
        res = storage.get(State, state_id)
        if res is None:
            abort(404)
        return jsonify(res.to_dict())
    else:
        return jsonify([m.to_dict() for m in storage.all(State).values()])


@app_views.route("/states/<state_id>", methods=["DELETE"])
def states_delete(state_id):
    """delete model object"""
    res = storage.get(State, state_id)
    if res is None:
        abort(404)
    storage.delete(res)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"])
def create_state():
    """create model object"""
    obj = request.get_json(force=True, silent=True)
    if not obj:
        abort(400, "Not a JSON")
    if "name" not in obj:
        abort(400, "Missing name")
    new_state = State(**obj)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """update model object"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    obj.name = data.get("name", obj.name)
    obj.save()
    return jsonify(obj.to_dict()), 200

#!/usr/bin/python3
"""Users objects API"""

from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"])
@app_views.route("/users/<user_id>", methods=["GET"])
def user(user_id=None):
    """get a user object or list of user""" 
    if user_id:
        res = storage.get(User, user_id)
        if res is None:
            abort(404)
        return jsonify(res.to_dict())
    else:
        return jsonify([m.to_dict() for m in storage.all(User).values()])

@app_views.route("/users/<user_id>", methods=["DELETE"])
def user_delete(user_id):
    """delete model object"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"])
def create_user():
    """create model object"""
    obj = request.get_json(force=True, silent=True)
    if not obj:
        abort(400, "Not a JSON")
    if "email" not in obj:
        abort(400, "Missing email")
    if "password" not in obj:
        abort(400, "Missing password")
    new_user = User(**obj)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """update user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    user.password = data.get("password", user.password)
    user.save()
    return jsonify(user.to_dict()), 200

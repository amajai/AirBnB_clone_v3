#!/usr/bin/python3
"""Amenities objects API"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, request, jsonify


@app_views.route("/amenities", methods=["GET"])
@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def amenity(amenity_id=None):
    """get a amenity object or list of amenities"""
    if amenity_id:
        res = storage.get(Amenity, amenity_id)
        if res is None:
            abort(404)
        return jsonify(res.to_dict())
    else:
        return jsonify([m.to_dict() for m in storage.all(Amenity).values()])


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def amenity_delete(amenity_id):
    """delete model object"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    """create model object"""
    obj = request.get_json(force=True, silent=True)
    if not obj:
        abort(400, "Not a JSON")
    if "name" not in obj:
        abort(400, "Missing name")
    new_amenity = Amenity(**obj)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """update amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    amenity.name = data.get("name", amenity.name)
    amenity.save()
    return jsonify(amenity.to_dict()), 200

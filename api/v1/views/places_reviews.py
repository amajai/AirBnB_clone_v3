#!/usr/bin/python3
"""Review objects API"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def reviews(place_id):
    """Get a model object or list of objects"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route("/reviews/<review_id>", methods=["GET"])
def reviews_id(review_id):
    """Get a Review object"""
    res = storage.get(Review, review_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def review_delete(review_id):
    """delete model object"""
    res = storage.get(Review, review_id)
    if res is None:
        abort(404)
    storage.delete(res)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """create a new Review object"""
    place = storage.get(Place, place_id)
    if place is None:
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
    if "text" not in obj:
        abort(400, "Missing text")
    new_review = Review(place_id=place.id, **obj)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """update review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    review.text = data.get("text", review.text)
    review.save()
    return jsonify(review.to_dict()), 200

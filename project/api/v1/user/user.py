from flask import request, current_app, jsonify, Blueprint
from flask.views import MethodView

from ..base import BaseAPI, token_required
from ....models.user import User
from ...common.utils.exceptions import NotImplementedException
from .... import db

bp = Blueprint("user", __name__)


@bp.route("/users", methods=["POST"])
def signup():
    """
    Sign up a new user.
    """
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing username or password"}), 400

    username = data["username"]
    password = data["password"]

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    user = User(username, password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


@bp.route("/users/me", methods=["GET"])
@token_required
def me(current_user):
    return current_user.json()

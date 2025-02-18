from flask import Blueprint, jsonify, request
from app.models.user import User
from app.extensions import db

user_api_bp = Blueprint("user_api", __name__)


@user_api_bp.route("/", methods=["GET"])
def get_users():
    users = User.query.all()
    user_list = [
        {"id": user.id, "name": user.name, "email": user.email} for user in users
    ]
    return jsonify(user_list)


@user_api_bp.route("/", methods=["POST"])
def create_user():
    data = request.json
    new_user = User(name=data["name"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully!"}), 201

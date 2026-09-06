from flask import Blueprint, jsonify, request

from controllers import user_controller

user_bp = Blueprint("users", __name__)


@user_bp.route("/users", methods=["GET"])
def get_users():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    result, status = user_controller.list_users(page, per_page)
    return jsonify(result), status


@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    result, status = user_controller.get_user(user_id)
    return jsonify(result), status


@user_bp.route("/users", methods=["POST"])
def create_user():
    result, status = user_controller.create_user(request.get_json())
    return jsonify(result), status


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    result, status = user_controller.update_user(user_id, request.get_json())
    return jsonify(result), status


@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    result, status = user_controller.delete_user(user_id)
    return jsonify(result), status


@user_bp.route("/users/<int:user_id>/tasks", methods=["GET"])
def get_user_tasks(user_id):
    result, status = user_controller.get_user_tasks(user_id)
    return jsonify(result), status


@user_bp.route("/login", methods=["POST"])
def login():
    result, status = user_controller.login(request.get_json())
    return jsonify(result), status

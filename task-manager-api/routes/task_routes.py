from flask import Blueprint, jsonify, request

from controllers import task_controller

task_bp = Blueprint("tasks", __name__)


@task_bp.route("/tasks", methods=["GET"])
def get_tasks():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    result, status = task_controller.list_tasks(page, per_page)
    return jsonify(result), status


@task_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    result, status = task_controller.get_task(task_id)
    return jsonify(result), status


@task_bp.route("/tasks", methods=["POST"])
def create_task():
    result, status = task_controller.create_task(request.get_json())
    return jsonify(result), status


@task_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    result, status = task_controller.update_task(task_id, request.get_json())
    return jsonify(result), status


@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    result, status = task_controller.delete_task(task_id)
    return jsonify(result), status


@task_bp.route("/tasks/search", methods=["GET"])
def search_tasks():
    result, status = task_controller.search_tasks(
        request.args.get("q", ""),
        request.args.get("status", ""),
        request.args.get("priority", ""),
        request.args.get("user_id", ""),
    )
    return jsonify(result), status


@task_bp.route("/tasks/stats", methods=["GET"])
def task_stats():
    result, status = task_controller.task_stats()
    return jsonify(result), status

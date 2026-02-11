from flask import Blueprint, request, jsonify
from app import db
from app.models import Budget

bp = Blueprint('budget', __name__, url_prefix='/budget')


# Set or update budget
@bp.route('', methods=['POST'])
def set_budget():
    data = request.get_json()

    if "monthly_limit" not in data:
        return jsonify({"error": "monthly_limit is required"}), 400

    # Only keep 1 budget record
    budget = Budget.query.first()

    if budget:
        budget.monthly_limit = data["monthly_limit"]
    else:
        budget = Budget(monthly_limit=data["monthly_limit"])
        db.session.add(budget)

    db.session.commit()

    return jsonify(budget.to_json()), 200


# Get budget
@bp.route('', methods=['GET'])
def get_budget():
    budget = Budget.query.first()

    if not budget:
        return jsonify({"message": "No budget set"}), 404

    return jsonify(budget.to_json()), 200

from flask import Blueprint, jsonify
from app.models import Subscription, Category, StatusType, FrequencyType
from app import db
from sqlalchemy.sql import func

bp = Blueprint('top_spending_category', __name__, url_prefix='/top-spending-category')

@bp.route('', methods=['GET'])
def top_spending_category():
    try:
        subscriptions = db.session.query(Subscription, Category.name)\
            .join(Category, Subscription.category_id == Category.id)\
            .filter(Subscription.status == StatusType.ACTIVE)\
            .all()

        if not subscriptions:
            return jsonify({"message": "No active subscriptions found"}), 404

        category_totals = {}

        for sub, cat_name in subscriptions:
            if sub.frequency == FrequencyType.WEEKLY:
                monthly_cost = sub.price * 4
            elif sub.frequency == FrequencyType.MONTHLY:
                monthly_cost = sub.price
            elif sub.frequency == FrequencyType.YEARLY:
                monthly_cost = sub.price / 12
            else:
                monthly_cost = 0

            category_totals[cat_name] = category_totals.get(cat_name, 0) + monthly_cost

        top_category_name = max(category_totals, key=category_totals.get)

        return jsonify({
            "category": top_category_name,
            "monthly_total": round(category_totals[top_category_name], 2)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

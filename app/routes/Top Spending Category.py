from sqlalchemy import func
from models import Subscription, Category
from app import db

bp = Blueprint('top-spending-category', __name__, url_prefix='/top-spending-category')

@bp.route('', methods=['GET'])
def top_spending_category():

    subscriptions = db.session.query(Subscription, Category)\
        .join(Category, Subscription.category_id == Category.id)\
        .filter(Subscription.status == StatusType.ACTIVE)\
        .all()

    category_totals = {}

    for sub, cat in subscriptions:
        if sub.frequency.value == "Weekly":
            monthly_cost = sub.price * 4
        elif sub.frequency.value == "Monthly":
            monthly_cost = sub.price
        elif sub.frequency.value == "Yearly":
            monthly_cost = sub.price / 12
        else:
            monthly_cost = 0

        category_totals[cat.name] = category_totals.get(cat.name, 0) + monthly_cost

    if not category_totals:
        return {"message": "No active subscriptions found"}, 404

    top_category = max(category_totals, key=category_totals.get)

    return {
        "category": top_category,
        "monthly_total": round(category_totals[top_category], 2)
    }

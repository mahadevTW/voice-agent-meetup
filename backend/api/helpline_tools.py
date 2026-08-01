"""Customer-support ("helpline") tool handlers.

Two responsibilities:
- Look up a customer's placed order for post-purchase support, by calling
  the same ecommerce-demo REST API used by shopping_tools.py.
- Answer policy questions (shipping, returns, payment, privacy, warranty)
  from the dummy policy documents in the policies/ directory.
"""

import logging

from backend.core.config import POLICIES_DIR
from backend.api.shopping_tools import get_json

logger = logging.getLogger("helpline_tools")

_POLICY_FILES = {
    "shipping": "shipping_policy.md",
    "returns": "returns_refunds_policy.md",
    "refunds": "returns_refunds_policy.md",
    "payment": "payment_policy.md",
    "privacy": "privacy_policy.md",
    "warranty": "warranty_policy.md",
}


def get_order_details(args: dict):
    order_id = args.get("order_id")
    if order_id is None:
        return {"error": "order_id is required"}

    orders = get_json("/api/orders")
    if isinstance(orders, dict) and orders.get("error"):
        return orders

    try:
        target_id = int(order_id)
    except (TypeError, ValueError):
        return {"error": f"'{order_id}' is not a valid order ID"}

    for order in orders or []:
        if order.get("id") == target_id:
            return order

    return {"error": f"No order found with ID {order_id}"}


def get_policy_info(args: dict):
    topic = (args.get("topic") or "").strip().lower()
    filename = _POLICY_FILES.get(topic)
    if filename is None:
        return {
            "error": f"Unknown policy topic '{topic}'",
            "available_topics": sorted(set(_POLICY_FILES.keys())),
        }

    path = POLICIES_DIR / filename
    if not path.exists():
        return {"error": f"Policy document for '{topic}' is missing"}

    return {"topic": topic, "policy_text": path.read_text(encoding="utf-8")}


HELPLINE_TOOL_HANDLERS = {
    "get_order_details": get_order_details,
    "get_policy_info": get_policy_info,
}

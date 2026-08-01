"""Shopping tool handlers.

Calls the ecommerce-demo REST API directly over HTTP (no MCP) — see
build-your-mcp-server-public/ecommerce-demo/app.py for the API being
consumed here. That service is unauthenticated and keeps a single global
cart (no per-user accounts), so these tools mirror that behavior.
"""

import logging
from typing import Optional

import requests

from backend.core.config import SHOPPING_API_BASE_URL

logger = logging.getLogger("shopping_tools")

_TIMEOUT = 10


def get_json(path: str, params: Optional[dict] = None):
    try:
        response = requests.get(f"{SHOPPING_API_BASE_URL}{path}", params=params, timeout=_TIMEOUT)
    except requests.RequestException as exc:
        logger.error("shopping API GET %s failed: %s", path, exc)
        return {"error": f"Could not reach the shopping service: {exc}"}
    return _to_result(response)


def post_json(path: str, json_body: Optional[dict] = None):
    try:
        response = requests.post(f"{SHOPPING_API_BASE_URL}{path}", json=json_body, timeout=_TIMEOUT)
    except requests.RequestException as exc:
        logger.error("shopping API POST %s failed: %s", path, exc)
        return {"error": f"Could not reach the shopping service: {exc}"}
    return _to_result(response)


def _to_result(response: requests.Response):
    try:
        body = response.json()
    except ValueError:
        body = response.text
    if response.status_code >= 400:
        detail = body.get("detail") if isinstance(body, dict) else body
        return {"error": detail or f"Shopping service returned HTTP {response.status_code}"}
    return body


def list_categories(args: dict):
    return {"categories": get_json("/api/categories")}


def search_items(args: dict):
    query = args.get("query")
    category = args.get("category")
    params = {}
    if query:
        params["q"] = query
    if category:
        params["category"] = category
    return {"items": get_json("/api/items", params=params)}


def get_item_details(args: dict):
    item_id = args.get("item_id")
    if item_id is None:
        return {"error": "item_id is required"}
    return get_json(f"/api/items/{item_id}")


def add_to_cart(args: dict):
    item_id = args.get("item_id")
    quantity = args.get("quantity", 1)
    if item_id is None:
        return {"error": "item_id is required"}
    return post_json("/api/cart", json_body={"item_id": item_id, "quantity": quantity})


def view_cart(args: dict):
    return get_json("/api/cart")


def place_order(args: dict):
    return post_json("/api/orders")


def get_order_history(args: dict):
    return {"orders": get_json("/api/orders")}


SHOPPING_TOOL_HANDLERS = {
    "list_categories": list_categories,
    "search_items": search_items,
    "get_item_details": get_item_details,
    "add_to_cart": add_to_cart,
    "view_cart": view_cart,
    "place_order": place_order,
    "get_order_history": get_order_history,
}

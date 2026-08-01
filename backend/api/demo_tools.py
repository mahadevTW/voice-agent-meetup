"""Toy demo tool handlers: weather, arithmetic, fake order status."""

_ORDERS = {
    "ORD-1001": "out for delivery, arriving in 20 minutes",
    "ORD-1002": "packed and waiting for pickup",
    "ORD-1023": "delivered yesterday at 6:45 PM",
}


def get_weather(args: dict):
    location = args.get("location", "unknown")
    return {
        "location": location,
        "temperature_c": 22,
        "condition": "sunny",
    }


def calculate(args: dict):
    expression = args.get("expression", "")
    allowed = set("0123456789+-*/(). ")
    if not expression or not set(expression) <= allowed:
        return {"error": "Only basic arithmetic is supported"}
    return {"expression": expression, "result": eval(expression, {"__builtins__": {}}, {})}


def get_order_status(args: dict):
    order_id = args.get("order_id", "")
    status = _ORDERS.get(order_id)
    if status is None:
        return {"order_id": order_id, "status": "not found"}
    return {"order_id": order_id, "status": status}


DEMO_TOOL_HANDLERS = {
    "get_weather": get_weather,
    "calculate": calculate,
    "get_order_status": get_order_status,
}

"""Realtime function-call schemas the model sees for every tool.

Every call is dispatched through the single POST /tools/call endpoint in
backend/api/tools.py. Schemas are grouped to match their handler file:
- demo_tools.py     -> DEMO_TOOL_SCHEMAS
- shopping_tools.py -> SHOPPING_TOOL_SCHEMAS
- helpline_tools.py -> HELPLINE_TOOL_SCHEMAS
"""

DEMO_TOOL_SCHEMAS = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get the current weather for a location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"},
            },
            "required": ["location"],
        },
    },
    {
        "type": "function",
        "name": "calculate",
        "description": "Evaluate a simple arithmetic expression, e.g. '12 * (3 + 4)'.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Arithmetic expression to evaluate"},
            },
            "required": ["expression"],
        },
    },
    {
        "type": "function",
        "name": "get_order_status",
        "description": "Look up the delivery status of an order by its order ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "Order ID, e.g. 'ORD-1023'"},
            },
            "required": ["order_id"],
        },
    },
]

SHOPPING_TOOL_SCHEMAS = [
    {
        "type": "function",
        "name": "list_categories",
        "description": "List all product categories available in the shop.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "search_items",
        "description": "Search for products by name/description and optionally filter by category.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search text, e.g. 'wireless headphones'"},
                "category": {"type": "string", "description": "Optional category name to filter by"},
            },
        },
    },
    {
        "type": "function",
        "name": "get_item_details",
        "description": "Get full details (price, description, category) for a single product by its item ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_id": {"type": "integer", "description": "The product's item ID"},
            },
            "required": ["item_id"],
        },
    },
    {
        "type": "function",
        "name": "add_to_cart",
        "description": "Add a product to the shopping cart, or increase its quantity if already in the cart.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_id": {"type": "integer", "description": "The product's item ID"},
                "quantity": {"type": "integer", "description": "How many units to add (default 1)"},
            },
            "required": ["item_id"],
        },
    },
    {
        "type": "function",
        "name": "view_cart",
        "description": "View the current contents of the shopping cart, including line totals and the grand total.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "place_order",
        "description": "Place an order for everything currently in the cart. Always confirm the cart contents with the customer before calling this.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "get_order_history",
        "description": "Get the full history of previously placed orders, newest first.",
        "parameters": {"type": "object", "properties": {}},
    },
]

HELPLINE_TOOL_SCHEMAS = [
    {
        "type": "function",
        "name": "get_order_details",
        "description": "Look up the full details of a specific previously placed order by its numeric order ID, for post-purchase support.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "Numeric order ID, e.g. '12'"},
            },
            "required": ["order_id"],
        },
    },
    {
        "type": "function",
        "name": "get_policy_info",
        "description": (
            "Get the official customer-support policy text for a topic, to answer questions about "
            "shipping, returns/refunds, payment, privacy, or warranty."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "One of: shipping, returns, refunds, payment, privacy, warranty",
                },
            },
            "required": ["topic"],
        },
    },
]

REALTIME_TOOLS = DEMO_TOOL_SCHEMAS + SHOPPING_TOOL_SCHEMAS + HELPLINE_TOOL_SCHEMAS

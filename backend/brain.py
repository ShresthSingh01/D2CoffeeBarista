import json
import os
from typing import Dict, Any

# Global order state
order_state = {
    "drinkType": None,
    "size": None,
    "milk": None,
    "extras": [],
    "name": None
}

drink_options = ["latte", "cappuccino", "americano", "espresso", "mocha"]
size_options = ["small", "medium", "large"]
milk_options = ["regular", "soy", "almond", "oat"]
extra_options = ["sugar", "vanilla", "caramel", "chocolate", "whipped cream"]


def reset_order():
    order_state["drinkType"] = None
    order_state["size"] = None
    order_state["milk"] = None
    order_state["extras"] = []
    order_state["name"] = None


def save_order(order):
    base_dir = os.path.dirname(__file__)
    orders_dir = os.path.join(base_dir, "orders")
    os.makedirs(orders_dir, exist_ok=True)

    path = os.path.join(orders_dir, "last_order.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(order, f, indent=4)


def think(text_input: str) -> Dict[str, Any]:
    text = text_input.lower().strip()

    # Manual restart
    if "start over" in text or "new order" in text:
        reset_order()
        return {"reply": "Starting a new order! What drink would you like?", "summary": None, "is_complete": False}

    # STEP 1 — DRINK
    if order_state["drinkType"] is None:
        for drink in drink_options:
            if drink in text:
                order_state["drinkType"] = drink
                return {"reply": "Great! What size — small, medium, or large?", "summary": None, "is_complete": False}
        return {"reply": "What drink would you like? Latte, cappuccino, americano, espresso, or mocha?", "summary": None, "is_complete": False}

    # STEP 2 — SIZE
    if order_state["size"] is None:
        for size in size_options:
            if size in text:
                order_state["size"] = size
                return {"reply": "Got it! What milk — regular, soy, almond, or oat?", "summary": None, "is_complete": False}
        return {"reply": "What size — small, medium, or large?", "summary": None, "is_complete": False}

    # STEP 3 — MILK
    if order_state["milk"] is None:
        for milk in milk_options:
            if milk in text:
                order_state["milk"] = milk
                return {"reply": "Any extras like sugar, vanilla, caramel, chocolate, or whipped cream? Say 'no extras' if none.", "summary": None, "is_complete": False}
        return {"reply": "Which milk — regular, soy, almond, or oat?", "summary": None, "is_complete": False}

    # STEP 4 — EXTRAS
    if order_state["extras"] == []:
        if "no" in text:
            order_state["extras"] = []
            return {"reply": "Great! And finally, what's your name?", "summary": None, "is_complete": False}

        for extra in extra_options:
            if extra in text:
                order_state["extras"].append(extra)

        return {"reply": "Anything else? If not, say 'no extras'.", "summary": None, "is_complete": False}

    # STEP 5 — NAME
    if order_state["name"] is None:
        order_state["name"] = text_input.title()

        summary = (
            f"{order_state['name']}'s order:\n"
            f"- {order_state['size'].title()} {order_state['drinkType'].title()}\n"
            f"- {order_state['milk'].title()} milk\n"
            f"- Extras: {', '.join(order_state['extras']) if order_state['extras'] else 'None'}"
        )

        save_order(order_state)
        reset_order()

        return {"reply": f"Thanks {order_state['name']}! Your order has been recorded.",
                "summary": summary,
                "is_complete": True}

    return {"reply": "I'm ready when you are!", "summary": None, "is_complete": False}

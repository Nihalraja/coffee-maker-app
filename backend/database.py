
from models import INVENTORY, ORDERS, COFFEE_MENU

def check_inventory(ingredients):
    """Check if ingredients are available in inventory."""
    for item, required_qty in ingredients.items():
        if INVENTORY.get(item, 0) < required_qty:
            return False, item
    return True, None

def update_inventory(ingredients):
    """Deduct the used ingredients from inventory."""
    for item, required_qty in ingredients.items():
        INVENTORY[item] -= required_qty

def place_order(coffee_id, quantity):
    """Place an order if inventory allows."""
    coffee = next((c for c in COFFEE_MENU if c["id"] == coffee_id), None)
    if not coffee:
        return {"error": "Coffee not found"}, 404

    ingredients_needed = {key: val * quantity for key, val in coffee["ingredients"].items()}
    is_available, missing_item = check_inventory(ingredients_needed)

    if not is_available:
        return {"error": f"Insufficient {missing_item}"}, 400

    update_inventory(ingredients_needed)
    total_price = coffee["price"] * quantity
    order = {
        "id": len(ORDERS) + 1,
        "coffee": coffee["name"],
        "quantity": quantity,
        "total_price": total_price
    }
    return {"message": "Order placed successfully!", "order": order}, 200

def refill_inventory(refill_data):
    """Refill inventory based on the provided data."""
    for item, qty in refill_data.items():
        if item in INVENTORY:
            INVENTORY[item] += qty
    return INVENTORY

def check_low_inventory(threshold=50):
    """Check for inventory items below the threshold."""
    return {item: qty for item, qty in INVENTORY.items() if qty < threshold}

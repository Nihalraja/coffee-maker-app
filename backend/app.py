from flask import Flask, jsonify, request
from flask_cors import CORS  
import json
import os
from models import COFFEE_MENU, INVENTORY, ORDERS, ADMIN_TOKEN, CoinModel

app = Flask(__name__)

CORS(app, origins=["http://localhost:8000"])  

ORDERS_FILE = 'orders.json'

def load_orders():
    """Load orders from the JSON file."""
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_orders(orders):
    """Save orders to the JSON file."""
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f, indent=4)

def is_admin(request):
    """Check if the request is authorized for admin actions."""
    token = request.headers.get("Authorization")
    return token == f"Bearer {ADMIN_TOKEN}"

@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify({"menu": COFFEE_MENU})

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify({"inventory": INVENTORY})

@app.route('/inventory/refill', methods=['POST'])
def handle_refill():
    if not is_admin(request):
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json
    updated_inventory = refill_inventory(data)
    return jsonify({"message": "Inventory updated successfully", "inventory": updated_inventory})

@app.route('/order', methods=['POST'])
def handle_order():
    data = request.json
    coffee_id = data.get("coffee_id")
    quantity = data.get("quantity", 1)
    user_name = data.get("user_name", "Guest")
    coin_data = data.get("coins", {})

    coins = CoinModel(
        quarters=coin_data.get("quarters", 0),
        dimes=coin_data.get("dimes", 0),
        nickels=coin_data.get("nickels", 0),
        pennies=coin_data.get("pennies", 0)
    )

    coffee = next((item for item in COFFEE_MENU if item["id"] == coffee_id), None)
    
    if not coffee:
        return jsonify({"error": "Coffee not found"}), 404
    
    total_price_cents = int(coffee["price"] * 100) * quantity  
    total_inserted_cents = int(coins.total_money() * 100)  
    
    if total_inserted_cents < total_price_cents:
        return jsonify({"error": "Insufficient funds"}), 400

    if INVENTORY["water"] < coffee["ingredients"].get("water", 0) * quantity:
        return jsonify({"error": "Not enough water"}), 400
    if INVENTORY["milk"] < coffee["ingredients"].get("milk", 0) * quantity:
        return jsonify({"error": "Not enough milk"}), 400
    if INVENTORY["coffee"] < coffee["ingredients"].get("coffee", 0) * quantity:
        return jsonify({"error": "Not enough coffee"}), 400

    INVENTORY["water"] -= coffee["ingredients"].get("water", 0) * quantity
    INVENTORY["milk"] -= coffee["ingredients"].get("milk", 0) * quantity
    INVENTORY["coffee"] -= coffee["ingredients"].get("coffee", 0) * quantity
    INVENTORY["money"] += total_price_cents / 100  

    order = {
        "coffee": coffee["name"],
        "quantity": quantity,
        "total_price": total_price_cents / 100,  
        "user_name": user_name
    }

    orders = load_orders()
    orders.append(order)
    save_orders(orders)

    return jsonify({"message": f"Here is your {coffee['name']}. Enjoy!"}), 200

@app.route('/orders', methods=['GET'])
def get_all_orders():
    return jsonify({"orders": load_orders()})

@app.route('/orders/<string:user_name>', methods=['GET'])
def get_user_orders(user_name):
    user_orders = [order for order in load_orders() if order["user_name"] == user_name]
    return jsonify({"user_orders": user_orders})

if __name__ == '__main__':
    app.run(debug=True)

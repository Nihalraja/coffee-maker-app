
COFFEE_MENU = [
    {"id": 1, "name": "Espresso", "price": 2.5, "ingredients": {"water": 50, "coffee": 18}}, 
    {"id": 2, "name": "Latte", "price": 3.5, "ingredients": {"water": 200, "milk": 150, "coffee": 24}},  
    {"id": 3, "name": "Cappuccino", "price": 3.0, "ingredients": {"water": 250, "milk": 100, "coffee": 24}}  
]

INVENTORY = {
    "water": 1000, 
    "milk": 500,    
    "coffee": 300,
    "money": 0
}

ORDERS = []

ADMIN_TOKEN = "secure_admin_token"  

class CoinModel:
    def __init__(self, quarters=0, dimes=0, nickels=0, pennies=0):
        self.quarters = quarters
        self.dimes = dimes
        self.nickels = nickels
        self.pennies = pennies

    def total_money(self):
        """Calculate the total amount of money inserted in dollars."""
        total = (self.quarters * 0.25) + (self.dimes * 0.10) + (self.nickels * 0.05) + (self.pennies * 0.01)
        return total

    def __repr__(self):
        return f"CoinModel(quarters={self.quarters}, dimes={self.dimes}, nickels={self.nickels}, pennies={self.pennies})"

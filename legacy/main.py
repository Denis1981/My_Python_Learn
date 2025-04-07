# main.py

from shopping_cart import ShoppingCart
from products import Smartphone, Clothing

cart = ShoppingCart("Алексей", "admin01")
cart.add_item(Smartphone("POCO", 22000, "P60", "чёрный"), 1)
cart.add_item(Clothing("Футболка", 1200, "M", "Хлопок"), 2)

print(cart.get_details())

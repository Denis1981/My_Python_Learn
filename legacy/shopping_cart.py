# shopping_cart.py

from products import Product, Smartphone, Clothing

class ShoppingCart:
    def __init__(self, customer_name, admin_name):
        self.customer_name = customer_name
        self.admin_name = admin_name
        self.items = []

    def add_item(self, product, quantity=1):
        for item in self.items:
            if item["Продукт"].name == product.name:
                item["количество"] += quantity
                return
        self.items.append({"Продукт": product, "количество": quantity})

    def remove_item(self, product_name):
        self.items = [item for item in self.items if item["Продукт"].name != product_name]

    def remove_one(self, product_name):
        for item in self.items:
            if item["Продукт"].name == product_name:
                item["количество"] -= 1
                if item["количество"] <= 0:
                    self.items.remove(item)
                break

    def get_total(self):
        return sum(item["Продукт"].price * item["количество"] for item in self.items)

    def get_details(self):
        details = f" Покупатель: {self.customer_name}\n"
        details += f" Корзина покупок:\n"
        for item in self.items:
            details += f"- {item['Продукт'].get_details()}, Кол-во: {item['количество']}\n"
        details += f"\n Общая сумма: {self.get_total():,.2f} руб\n"
        details += f" Заказ оформил: {self.admin_name}"
        return details

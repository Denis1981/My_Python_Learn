# products.py

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_details(self):
        return f"Продукт: {self.name}, Цена: {self.price} руб."

# новый тип продукта, к примеру Смартфоны
class Smartphone(Product):
    def __init__(self, name, price, model, color):
        super().__init__(name, price)
        self.model = model
        self.color = color

    def get_details(self):
        return f"Смартфон: {self.name}, Модель: {self.model}, Цвет: {self.color}, Цена: {self.price} руб."


class Clothing(Product):
    def __init__(self, name, price, size, material):
        super().__init__(name, price)
        self.size = size
        self.material = material

    def get_details(self):
        return f"Одежда: {self.name}, Размер: {self.size}, Материал: {self.material}, Цена: {self.price} руб."

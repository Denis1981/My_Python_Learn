class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name}: {self.price} руб."

    def __repr__(self):
        return f"Product(name={self.name}, price={self.price})"

    def __eq__(self, other):
        return self.price == other.price

    def __lt__(self, other):
        return self.price < other.price


class Discount:
    def __init__(self, description, discount_percent):
        self.description = description
        self.discount_percent = discount_percent

    def __str__(self):
        return f"Скидка: {self.description} ({self.discount_percent}%)"

    def __repr__(self):
        return f"Discount(description={self.description}, discount_percent={self.discount_percent})"

    @staticmethod
    def apply_discount(price, discount_percent):
        return price * (1 - discount_percent / 100)

    @staticmethod
    def seasonal_discount(order):
        return sum(Discount.apply_discount(product.price, 10) for product in order.products)

    @staticmethod
    def promo_code_discount(order, promo_percent):
        return sum(Discount.apply_discount(product.price, promo_percent) for product in order.products)


class Order:
    total_orders = 0
    total_revenue = 0

    def __init__(self, products, discount=None):
        self.products = products
        self.discount = discount
        Order.total_orders += 1
        self.total_price = self.calculate_total_price()
        Order.total_revenue += self.total_price

    def __str__(self):
        return f"Заказ из {len(self.products)} товаров, сумма: {self.total_price} руб."

    def __repr__(self):
        return f"Order(products={self.products}, total_price={self.total_price})"

    def calculate_total_price(self):
        if self.discount:
            return sum(
                Discount.apply_discount(product.price, self.discount.discount_percent) for product in self.products)
        return sum(product.price for product in self.products)

    @classmethod
    def get_total_orders(cls):
        return cls.total_orders

    @classmethod
    def get_total_revenue(cls):
        return cls.total_revenue


class Customer:
    def __init__(self, name):
        self.name = name
        self.orders = []

    def __str__(self):
        return f"Клиент: {self.name}, Заказы: {len(self.orders)}"

    def __repr__(self):
        return f"Customer(name={self.name}, orders={len(self.orders)})"

    def add_order(self, order):
        self.orders.append(order)

    def get_total_spent(self):
        return sum(order.total_price for order in self.orders)


# Создание продуктов
p1 = Product("Ноутбук", 70000)
p2 = Product("Смартфон", 50000)
p3 = Product("Планшет", 30000)

# Создание клиентов
c1 = Customer("Иван")
c2 = Customer("Ольга")

# Создание скидок
seasonal_discount = Discount("Сезонная скидка", 10)
promo_discount = Discount("Скидка по промокоду", 15)

# Создание заказов
order1 = Order([p1, p2], seasonal_discount)
order2 = Order([p3], promo_discount)

# Добавление заказов клиентам
c1.add_order(order1)
c2.add_order(order2)

# Вывод информации о клиентах, заказах и общей статистике
print(c1)
print(c2)
print(order1)
print(order2)
print(f"Общее количество заказов: {Order.get_total_orders()}")
print(f"Общая сумма всех заказов: {Order.get_total_revenue()} руб.")
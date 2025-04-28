class Order:
    def __init__(self, order_id, product_name, quantity):
        self.order_id = order_id
        self.product_name = product_name
        self.quantity = quantity

    def __str__(self):
        return f"Sipariş ID: {self.order_id} - {self.product_name} - Miktar: {self.quantity}"
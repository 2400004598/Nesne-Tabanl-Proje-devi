import json

class Product:
    def __init__(self, name, stock_quantity):
        self.name = name
        self.stock_quantity = stock_quantity

    def to_dict(self):
        return {"name": self.name, "stock_quantity": self.stock_quantity}

    @staticmethod
    def from_dict(data):
        return Product(data['name'], data['stock_quantity'])

class Stock:
    def __init__(self, filename="stok.json"):
        self.products = {}
        self.filename = filename
        self.load_products()

    def add_product(self, product):
        if product.name in self.products:
            self.products[product.name].stock_quantity += product.stock_quantity
        else:
            self.products[product.name] = product
        self.save_products()

    def get_product(self, name):
        return self.products.get(name)

    def update_product(self, name, stock_quantity):
        if name in self.products:
            self.products[name].stock_quantity = stock_quantity
            self.save_products()

    def remove_product(self, name):
        if name in self.products:
            del self.products[name]
            self.save_products()

    def load_products(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                self.products = {product_data["name"]: Product.from_dict(product_data) for product_data in data}
        except (FileNotFoundError, json.JSONDecodeError):
            self.products = {}

    def save_products(self):
        with open(self.filename, "w") as file:
            data = [product.to_dict() for product in self.products.values()]
            json.dump(data, file)
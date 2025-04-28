class Stock:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        self.products[product.name] = product

    def update_product_stock(self, product_name, quantity):
        if product_name in self.products:
            self.products[product_name].update_stock(quantity)

    def show_stock(self):
        for product in self.products.values():
            print(product)
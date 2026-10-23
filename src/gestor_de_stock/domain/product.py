class Product:
    def __init__(
        self,
        id: int | None,
        name: str,
        price: float,
        quantity: int,
        category_id: int | None = None,
    ):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category_id = category_id
        if price < 0:
            raise ValueError("price cannot be negative")
        if quantity < 0:
            raise ValueError("quantity cannot be negative")

    def show_info(self):
        print("ID:", self.id)
        print("Name: ", self.name)
        print("Price: ", self.price)
        print("Quantity: ", self.quantity)
        print("Category ID: ", self.category_id)

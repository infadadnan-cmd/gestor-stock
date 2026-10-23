class ProductWithCategory:
    def __init__(
        self,
        id: int,
        name: str,
        price: float,
        quantity: int,
        category_id: int | None,
        category_name: str | None,
    ):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category_id = category_id
        self.category_name = category_name

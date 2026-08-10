class Product:
    def __init__(self, name, price, id= None):
        self.id= id
        self.name= name
        self.price= price
    def show_info(self):
        print("ID:", self.id)
        print("Name: ", self.name)
        print("Price: ", self.price)
    @classmethod
    def from_row(cls, row):
     return cls(
        name= row["name"],
        price= row["price"],
        id= row["id"]
    )
    



mouse= Product(6, "Mouse", 10)
Usb= Product(8, "Usb",15)

    
    
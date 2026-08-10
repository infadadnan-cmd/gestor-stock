from product import Product
import database


class Inventory:

    def get_all_products(self):
      return database.get_all_products()

    def add_product(self, product: Product) -> Product:
        return database.insert_product(product)
    def find_product(self, id):
        return database.find_product(id)
        
    def remove_product(self,id) -> bool: 
        return database.delete_product(id)
    
    def update_product(self,id, name, price):
        return database.update_product(id, name, price)
    def total_price(self):
        total_price= 0
        for product in self.products: 
            total_price= total_price + product.price
        return total_price


   
       
       

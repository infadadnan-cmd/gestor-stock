import os
from product import Product
from inventory import Inventory
import validators
import database
database.create_table()
inventory= Inventory()

while True:
    print(1, "Show products")
    print(2, "Add product")
    print(3, "Find product")
    print(4, "Remove product")
    print(5, "Total inventroy value")
    print(6, "Update product price")
    print(7, "Exit")
    option= input("choose an option ")
    if option== "1":
        inventory.show_inventory()
    elif option== "2":
        name= validators.get_valid_name()
        price= validators.get_valid_price()
        product= Product(None, name, price)
        inventory.add_product(product)     
    elif option== "3":
        id= validators.get_valid_id()
        product= inventory.find_product(id)
        if product is not None:
            product.show_info()
        else: 
            print("Product not found! ")          
    elif option== "4":
        id= validators.get_valid_id()
        if inventory.remove_product(id):
            print("product removed! ")
        else:
            print("Product not found: ")
    elif option== "5":
        total= inventory.total_price()
        print("Total price is: ",total)
    elif option== "6":
        id= int(input("Enter product id: "))
        new_price= int(input("Enter new_price: "))
        if inventory.update_price(id, new_price):
            print("Product price changed succesfuly! ")
        else: 
            print("product not found! ")      
    elif option== "7":
        inventory.save_products()
        print("goodbye!")
        break
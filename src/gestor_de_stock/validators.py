def get_valid_price():
 while True:
    try:
      price= int(input("Enter new price: "))
      if is_valid_price(price):
         return price
      print("number must be great than 0")
    except ValueError:
        print("invalid price")
              
def is_valid_price(price):
    return price > 0   

def get_valid_name():
   while True:
      name= input("Enter valid name: ")
      if is_valid_name(name):
         return name
      print("Invalid name!")

def is_valid_name(name):
   return name.isalpha()
def is_valid_id(id):
   return id> 0
def get_valid_id():
   while True:
      try:
        id= int(input("Enter id: "))
        if is_valid_id(id):
           return id
      except ValueError:
         print("Invalid id!")
         
      

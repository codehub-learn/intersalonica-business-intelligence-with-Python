import finance
import logging

customer1 = {
    "name": "John Doe",
    "age": 30,
    "city": "New York",
    "email": "doe@mail.com"
}
customer2 = {
    "name": "Jane Smith",
    "age": 25,
    "city": "Los Angeles",
    "email": "smith@email.com"
}

db_table = [customer1, customer2]

customer1["age"] = 31
customer1["phone"] = "123-456-7890"
customer1["ammount"] = finance.interest_calculation(1000, 0.05, 5)
print(customer1)


account1 = finance.Account(1, "John Doe",1000 )
account1.deposit(500)

logging.basicConfig(level=logging.INFO)
logging.info(f"Account balance: {account1.balance}")    
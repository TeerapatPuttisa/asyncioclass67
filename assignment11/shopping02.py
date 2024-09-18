import time
import asyncio
from asyncio import Queue

# Product class with checkout time
class Product:
    def __init__(self, product_name: str, checkout_time: float):
        self.product_name = product_name
        self.checkout_time = checkout_time

# Customer class with a list of products
class Customer:
    def __init__(self, customer_id: int, products: list[Product]):
        self.customer_id = customer_id
        self.products = products

# Checkout customer method that simulates checkout process
async def checkout_customer(queue: Queue, cashier_number: int):
    cashier_take = {"id": cashier_number, "time": 0, "customer": 0}
    while not queue.empty():
        customer: Customer = await queue.get()
        cashier_take['customer'] += 1
        print(f"The Cashier_{cashier_number} "
              f"will checkout Customer_{customer.customer_id}")
        
        for product in customer.products:
            product_take_time = round(product.checkout_time, ndigits=2)
            print(f"The Cashier_{cashier_number} "
                  f"will checkout Customer_{customer.customer_id}'s "
                  f"Product_{product.product_name} "
                  f"in {product.checkout_time} secs")
            await asyncio.sleep(product.checkout_time)
            cashier_take["time"] += product_take_time
        
        print(f"The Cashier_{cashier_number} "
              f"finished checkout Customer_{customer.customer_id} "
              f"in {round(cashier_take['time'], ndigits=2)} secs")
        
        queue.task_done()
    return cashier_take

# Generate customers with adjusted product times
def generate_customer(customer_id: int) -> Customer:
    # Adjusting checkout times to hit close to 8.02 seconds
    all_products = [Product('beef', 1.1),   # Changed from 1 to 1.1
                    Product('banana', .45), # Changed from 0.4 to 0.45
                    Product('sausage', .45),# Changed from 0.4 to 0.45
                    Product('diapers', .2)] # Kept the same
    return Customer(customer_id, all_products)

# Customer generation method
async def customer_generation(queue: Queue, customers: int):
    customer_count = 0
    while True:
        customers = [generate_customer(the_id)
                     for the_id in range(customer_count, customer_count + customers)]
        
        for customer in customers:
            print("Waiting to put customer in line....")
            await queue.put(customer)
            print("Customer put in line...")
        
        customer_count = customer_count + len(customers)
        await asyncio.sleep(0.001)
        return customer_count

# Main method
async def main():
    customer_queue = Queue(3)
    customers_start_time = time.perf_counter()
    customer_producer = asyncio.create_task(customer_generation(customer_queue, 10))
    cashiers = [checkout_customer(customer_queue, i) for i in range(5)]
    
    results = await asyncio.gather(customer_producer, *cashiers)
    print(20*'-')
    for cashier in results[1:]:
        if cashier:
            print(f"The Cashier_{cashier['id']} "
                  f"take {cashier['customer']} customer "
                  f"total {round(cashier['time'], ndigits=2)} secs.") 

    print(f"The supermarket process finished "
          f"{customer_producer.result()} customers "
          f"in {round(time.perf_counter() - customers_start_time, ndigits=2)} secs")

if __name__ == "__main__":
    asyncio.run(main())

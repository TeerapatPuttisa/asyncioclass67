import time
import asyncio
from asyncio import Queue

# Product class represents products that need to be checked out, each with a checkout time.
class Product:
    def __init__(self, product_name: str, checkout_time: float):
        self.product_name = product_name
        self.checkout_time = checkout_time

# Customer class represents a customer with an ID and list of products
class Customer:
    def __init__(self, customer_id: int, products: list[Product]):
        self.customer_id = customer_id
        self.products = products

# Cashier process simulating the checkout process for each customer in the queue.
async def checkout_customer(queue: Queue, cashier_number: int):
    cashier_take = {"id": cashier_number, "time": 0, "customer": 0}
    
    while not queue.empty():
        customer: Customer = await queue.get()  # Get customer from the queue
        
        cashier_take['customer'] += 1  # Count how many customers this cashier has served
        print(f"Cashier_{cashier_number} is checking out Customer_{customer.customer_id}")
        
        for product in customer.products:  # Iterate through products in the customer's cart
            product_take_time = round(product.checkout_time, ndigits=2)
            print(f"Cashier_{cashier_number} will checkout Customer_{customer.customer_id}'s Product_{product.product_name} in {product.checkout_time} secs")
            await asyncio.sleep(product.checkout_time)  # Simulate checkout time for the product
            cashier_take["time"] += product_take_time  # Add the time for this product to the cashier's total time
        
        print(f"Cashier_{cashier_number} finished checkout for Customer_{customer.customer_id} in {round(cashier_take['time'], ndigits=2)} secs")
        
        queue.task_done()  # Mark the task as done
    return cashier_take

# Function to generate customers with products based on the data
def generate_customer(customer_id: int, products: list[Product]) -> Customer:
    return Customer(customer_id, products)

# Asynchronous function to generate customers and place them in the queue.
async def customer_generation(queue: Queue, customers_data: list):
    for customer_data in customers_data:
        customer = generate_customer(customer_data['id'], customer_data['products'])
        print(f"Putting Customer_{customer.customer_id} into the queue.")
        await queue.put(customer)  # Put the customer into the queue
        await asyncio.sleep(0.001)  # Simulate slight delay between customer arrivals
    
    await queue.join()  # Wait until all tasks are done
    return len(customers_data)

# Main function to run the simulation
async def main():
    customer_queue = Queue()
    
    # Data representing customers and their products (with checkout times)
    customers_data = [
        {'id': 1, 'products': [Product('Product_1', 2.0), Product('Product_2', 2.4)]},
        {'id': 2, 'products': [Product('Product_1', 4.0), Product('Product_2', 2.4)]},
        {'id': 3, 'products': [Product('Product_1', 4.0), Product('Product_2', 4.8)]},
        {'id': 4, 'products': [Product('Product_1', 2.0), Product('Product_2', 2.4), Product('Product_3', 0.4), Product('Product_4', 3.2), Product('Product_5', 3.6)]},
        {'id': 5, 'products': [Product('Product_1', 4.0), Product('Product_2', 2.0), Product('Product_3', 3.2), Product('Product_4', 3.6)]}
    ]
    
    # Generate customers and put them into the queue
    customer_producer = asyncio.create_task(customer_generation(customer_queue, customers_data))
    
    # Create checkout tasks for cashiers
    cashiers = [checkout_customer(customer_queue, i+1) for i in range(4)]  # 4 cashiers
    
    # Wait for all tasks to complete
    results = await asyncio.gather(customer_producer, *cashiers)
    
    print(20 * '-')
    # Print out the result for each cashier
    for cashier in results[1:]:
        if cashier:
            print(f"Cashier_{cashier['id']} served {cashier['customer']} customers in total time: {round(cashier['time'], 2)} secs.")
    
    print(f"Total customers processed: {results[0]}")

# Run the asynchronous event loop
if __name__ == "__main__":
    asyncio.run(main())

from aiokafka import AIOKafkaProducer
import asyncio
from aiokafka.errors import KafkaError

async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()  # Start the producer
    
    try:
        while True:
            try:
                # Produce message
                pr = await producer.send_and_wait("my_topic", b"Super message")
                print(pr)
                await asyncio.sleep(1)
            
            except KafkaError as e:
                print(f"Kafka error occurred: {e}")
                break  # You can handle this differently if needed
                
    finally:
        # Ensure producer stops in both normal and error situations
        print("Stopping producer...")
        await producer.stop()
# Run the async function
asyncio.run(send_one())

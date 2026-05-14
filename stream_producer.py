import json
import time
import random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

print("🚀 Producer started. Sending transactions to Kafka...")

while True:
    data = {
        "amount": round(random.uniform(10, 1000), 2),
        "is_international": random.choice([0, 1]),
        "user_id": random.randint(1000, 9999)
    }
    producer.send('transactions', value=data)
    print(f"📤 Sent to Kafka: {data}")
    time.sleep(1)
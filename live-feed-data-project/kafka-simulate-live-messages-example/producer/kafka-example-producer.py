'''

This kafka producer will simulate sending raw
'''


from kafka import KafkaProducer
from faker import Faker
import json

# Use the DOCKER listener port (exposed as host.docker.internal:29092)
producer = KafkaProducer(
    bootstrap_servers=['kafka1:29092', 'kafka2:29093', 'kafka3:29094'],
   value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    name = Faker().name()
    text = Faker().text()
    topic = 'Ppl-Text'
    message = f'{name}> {text}'


    data = {'person': name, 'text': message}

    # Send message
    producer.send(topic, value=data)
    producer.flush()

    print(f"✅ Sent message to topic '{topic}': {message}")



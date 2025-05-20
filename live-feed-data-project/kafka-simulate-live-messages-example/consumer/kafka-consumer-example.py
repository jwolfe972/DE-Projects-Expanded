from kafka import KafkaConsumer
import psycopg2
import sys
import json


try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        dbname="de-projects-db",
        user="user",
        password="password"
    )

    conn.autocommit = False

    cursor = conn.cursor()


    print("Connecting to PostgreSQL")

    cursor.close()
    conn.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(f'Connection to DB Error: {error}')
    sys.exit(1)


consumer = KafkaConsumer(

    'Faker_Example',
    bootstrap_servers=['localhost:9092', 'localhost:9093', 'localhost:9094'],
    group_id='demo-group',
    auto_offset_reset='earliest',
    enable_auto_commit=False
)

try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        dbname="de-projects-db",
        user="user",
        password="password"
    )


    conn.autocommit = False
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS kafka_messages(
        id SERIAL PRIMARY KEY,
        content JSONB,
        received TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')


    conn.commit()
    print(f'Table created successfully')
except (Exception, psycopg2.DatabaseError) as error:
    print(f'Create table Error: {error}')
    sys.exit(1)


try:
    while True:
        records = consumer.poll(timeout_ms=1000)
        for topic, messages in records.items():
            for message in messages:
                try:
                    data = message.value
                    if isinstance(data, bytes):
                        data = json.loads(data)
                    print(f'Received message {topic}: {data}')
                    cursor.execute('INSERT INTO kafka_messages (content) VALUES (%s);',
                                   [json.dumps(data)])
                    conn.commit()
                    consumer.commit()
                except Exception as e:
                    print(f'Exception: {e}')
                    conn.rollback()
                    consumer.commit()
except KeyboardInterrupt:
    print(f'Shutting down...')

finally:
    consumer.close()
    cursor.close()
    conn.close()
    print("Done")



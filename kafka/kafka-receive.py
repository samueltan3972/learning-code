from kafka import KafkaConsumer

def consume_messages(topic):
    consumer = KafkaConsumer(topic,
                             bootstrap_servers='localhost:9092',
                             value_deserializer=lambda v: str(v).decode('utf-8'))

    try:
        while True:
            messages = consumer.poll()
            for topic, data in messages.items():
                for message in data:
                    print(f"Received message: {message.value}")
            consumer.commit()
    except Exception as e:
        print(f"Error consuming messages: {e}")
    finally:
        consumer.close()

# Example usage
consume_messages("my_topic")
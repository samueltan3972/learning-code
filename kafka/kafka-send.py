from kafka import KafkaProducer

def send_message(message, topic):
    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: str(v).encode('utf-8'))

    try:
        producer.send(topic, key=b'15', value=message)
        producer.flush()
        print(f"Message '{message}' sent to topic '{topic}'")
    except Exception as e:
        print(f"Error sending message: {e}")
    finally:
        producer.close()
        pass

# Example usage
send_message("Hello, Kafka!", "my_topic2")
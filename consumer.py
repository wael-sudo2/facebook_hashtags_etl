import json
from kafka import KafkaConsumer, KafkaProducer
def consumer():
    kafka_server = ['127.0.0.1:9092']
    topic = "testtopic"

    consumer = KafkaConsumer(
        bootstrap_servers=kafka_server,
        value_deserializer=lambda m: json.loads(m.decode("ascii")),
        auto_offset_reset="earliest",
    )
    consumer.subscribe(topic)
    
    try:
        while True:
            data = next(consumer)
            print(data)
            yield data.value
    except StopIteration:
        print("break")
if __name__ == '__main__':
    consumer()
import json
from datetime import datetime
from time import sleep
from random import choice
from kafka import KafkaProducer
import time
def producer():
    kafka_server = ['127.0.0.1:9092']

    topic = "testtopic"

    producer = KafkaProducer(
        bootstrap_servers=kafka_server,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    with open('data.json', 'r') as json_file:
        json_list = list(json_file)
    iter_list = iter(json_list)
    try:
        while True:
            
                element = next(iter_list)
                producer.send(topic, element)
                producer.flush()
                time.sleep(1)
    except StopIteration:
        print(f'sent {len(json_list)} element ..../')

if __name__ == '__main__':
    producer()

import logging
import uuid

from confluent_kafka import Producer, Consumer


def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


class KafkaClient:
    def __init__(self, config):
        config['group.id'] = str(uuid.uuid1())
        self.producer = Producer(**config)
        config['group.id'] = str(uuid.uuid1())
        self.consumer = Consumer(**config)

    def send_data(self, topic_name, message):
        try:
            self.producer.produce(topic_name, message, key=str(uuid.uuid4()), callback=delivery_report)
        except Exception as e:
            logging.error(e)

    def flush_data(self):
        try:
            self.producer.flush()
        except Exception as e:
            logging.error(e)

    def subscribe(self, topic_names):
        self.consumer.subscribe(topic_names)

    def close_consumer(self):
        self.consumer.close()

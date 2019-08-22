from confluent_kafka import KafkaException, KafkaError
import json
import logging

from app.src.util.summary_utils import validate_json


class SummaryDataReader:

    def __init__(self, kafka_client, summary_topic_name):
        self.kafka_client = kafka_client
        self.summary_topic_name = summary_topic_name

    def read_summary(self):
        print('SummaryDataReader  is ready to consume the data from %s' % self.summary_topic_name)
        self.kafka_client.subscribe([self.summary_topic_name])
        try:
            while True:
                msg = self.kafka_client.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    # Error or event
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        print('%% %s [%d] reached end at offset %d\n' %
                              (msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        # Error
                        raise KafkaException(msg.error())
                else:
                    # Proper message
                    print('%% %s [%d] at offset %d with key %s:\n' %
                          (msg.topic(), msg.partition(), msg.offset(),
                           str(msg.key())))
                    print(msg.value())
        except Exception as err:
            logging.error(err)

        # Close down consumer to commit final offsets.
        finally:
            self.kafka_client.close_consumer()

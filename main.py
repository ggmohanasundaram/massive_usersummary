import argparse
import logging
import threading

from app.src.data.detail_data_generator import DetailDataGenerator
from app.src.data.summary_data_generator import SummaryDataGenerator
from app.src.data.summary_data_reader import SummaryDataReader
from app.src.util.kafkaclient import KafkaClient
from app.src.util.summary_utils import read_config

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--configname', help="Configuration File", type=str)
    parser.add_argument('--messagecount', help="Number of raw messages", type=int)
    args = parser.parse_args()
    config = args.configname
    count = args.messagecount if args.messagecount is not None else 50
    if config is not None:
        connection_info = read_config(config)
        kafka_client = KafkaClient(connection_info['kafka']['connection'])

        data_generator = DetailDataGenerator(kafka_client, connection_info['kafka']['raw_topic'])

        summary_data_generator = SummaryDataGenerator(kafka_client, connection_info['kafka']['raw_topic'],
                                                      connection_info['kafka']['summary_topic'])

        summary_data_reader = SummaryDataReader(kafka_client, connection_info['kafka']['summary_topic'])

        producer_thread = threading.Thread(target=data_generator.publish_raw_data, args=(count,))
        consumer_thread = threading.Thread(target=summary_data_generator.consume_raw_data)
        summary_consumer_thread = threading.Thread(target=summary_data_reader.read_summary)
        print("Start the consumer_thread and producer_thread")
        consumer_thread.start()
        producer_thread.start()
        summary_consumer_thread.start()
        producer_thread.join()

    else:
        logging.error("Config Name is missing ")

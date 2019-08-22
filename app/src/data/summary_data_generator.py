from confluent_kafka import KafkaException, KafkaError
import json
import logging

from app.src.util.summary_utils import validate_json


class SummaryDataGenerator:

    def __init__(self, kafka_client, raw_topic_name, summary_topic_name):
        self.kafka_client = kafka_client
        self.raw_topic_name = raw_topic_name
        self.summary_topic_name = summary_topic_name
        self.summary_details = []
        self.user_summary = {}
        self.invalid_user_data = []

    def consume_raw_data(self):
        print('SummaryDataGenerator  is ready to consume the data from %s' % self.raw_topic_name)
        self.kafka_client.subscribe([self.raw_topic_name])
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
                    self.createDataSummary(msg.value(), msg.key())
        except Exception as err:
            logging.error(err)
        # Close down consumer to commit final offsets.
        finally:
            self.kafka_client.close_consumer()

    def createDataSummary(self, inputData, key):
        try:
            raw_user_data = json.loads(inputData)
            # Validate the raw data against the json schema
            isValid = validate_json(raw_user_data, 'visitor_schema')
            if isValid:
                if raw_user_data['userId'] in self.user_summary:
                    userid = raw_user_data['userId']
                    is_last_seen_changed = False
                    if raw_user_data['Metadata']['timestamp'] < self.user_summary[userid]['firstSeen']:
                        self.user_summary[userid]['firstSeen'] = raw_user_data['Metadata']['timestamp']
                        is_last_seen_changed = True
                    if raw_user_data['Metadata']['timestamp'] > self.user_summary[userid]['lastSeen']:
                        self.user_summary[userid]['lastSeen'] = raw_user_data['Metadata']['timestamp']
                        is_last_seen_changed = True
                    # if either firstSeen or lastSeen time has been changed,
                    # publish the message to Summary Topic
                    if is_last_seen_changed:
                        print('Change in Summary for user %s' % userid)
                        summary_report = {}
                        summary_report['userId'] = userid
                        summary_report['firstSeen'] = self.user_summary[userid]['firstSeen']
                        summary_report['lastSeen'] = self.user_summary[userid]['lastSeen']
                        self.kafka_client.send_data(self.summary_topic_name, json.dumps(summary_report))
                        self.kafka_client.flush_data()
                        print('Changes Pushed  for user %s' % userid)
                else:
                    print('New User %s has been identified  ' % raw_user_data['userId'])
                    self.user_summary[raw_user_data['userId']] = {'firstSeen': raw_user_data['Metadata']['timestamp'],
                                                                  'lastSeen': raw_user_data['Metadata']['timestamp']}
            else:
                print('Invalid message %s has been identified' % self.invalid_user_data.append(key))
                self.invalid_user_data.append(key)
        except Exception as err:
            self.invalid_user_data.append(key)
            logging.error('Exception in createDataSummary %s' % str(err))
            logging.error(err)

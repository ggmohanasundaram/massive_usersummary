import time
import uuid
import json
import random


class DetailDataGenerator:
    def __init__(self, kafka_client, topic_name):
        self.kafka_client = kafka_client
        self.topic_name = topic_name

    # Generate number of Raw data based on count
    def publish_raw_data(self, count):
        print(" Total Number of messages %d " % count)
        for i in range(count):
            message = json.dumps(self.prepare_data())
            self.kafka_client.send_data(self.topic_name, message)
            time.sleep(5)
        self.kafka_client.flush_data()
        print("%d RAW Messages have been delivered " % count)

    # Generate the random raw data
    def prepare_data(self):
        user_details = {}
        userId_list = ["j11288090", "j11288091", "j11288092", "j11288093", "j11288094", "j11288095", "j11288096",
                       "j11288097", "j11288098", "j11288099"]
        userId = userId_list[random.randint(0, len(userId_list) - 1)]
        user_details['userId'] = userId
        user_details['visitorId'] = str(uuid.uuid4())
        user_details['type'] = 'Event'
        user_details['Metadata'] = {}
        user_details['Metadata']['messageId'] = str(uuid.uuid4())
        user_details['Metadata']['sentAt'] = round(time.time())
        user_details['Metadata']['timestamp'] = round(time.time())
        user_details['Metadata']['receivedAt'] = 0
        user_details['Metadata']['apiKey'] = ''
        user_details['Metadata']['apiKey'] = ''
        user_details['Metadata']['spaceId'] = ''
        user_details['Metadata']['version'] = ''
        user_details['event'] = 'Played Movie'
        user_details['eventData'] = {}
        user_details['eventData']['MovieID'] = str(uuid.uuid4())
        return user_details

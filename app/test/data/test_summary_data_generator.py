import unittest
from unittest.mock import patch, Mock

from app.src.data.summary_data_generator import SummaryDataGenerator

input = """{
    "userId": "jas8v98171",
    "visitorId": "jas8v98171",
    "type": "Mohanannsnndfaafa",
    "Metadata": {
        "messageId": "123sfdafas-32487239857dsh98234",
        "sentAt": 1534382478,
        "timestamp": 1534382478,
        "receivedAt": 0,
        "apiKey": "",
        "spaceId": "",
        "version": "v1"
    },
    "event": "Played Movie",
    "eventData": {
        "MovieID": "MIM4ddd4"
    }
}"""


class TestSummaryDataGenerator(unittest.TestCase):
    def test_publish_raw_data_for_new_user(self):
        client = Mock()
        client.send_data.return_value = None
        generator = SummaryDataGenerator(client, 'some_detail_topic', 'some_summary_topic')
        generator.createDataSummary(input, 'key')
        self.assertEqual({'jas8v98171': {'firstSeen': 1534382478, 'lastSeen': 1534382478}},
                         generator.user_summary)

    def test_publish_raw_data_with_existing_user(self):
        client = Mock()
        client.send_data.return_value = None
        generator = SummaryDataGenerator(client, 'some_detail_topic', 'some_summary_topic')
        generator.user_summary = {'jas8v98171': {'firstSeen': 1434382478, 'lastSeen': 1434382478}}
        generator.createDataSummary(input, 'key')
        self.assertEqual({'jas8v98171': {'firstSeen': 1434382478, 'lastSeen': 1534382478}},
                         generator.user_summary)
        generator.user_summary = {'jas8v98171': {'firstSeen': 1634382478, 'lastSeen': 1434382478}}
        generator.createDataSummary(input, 'key')
        self.assertEqual({'jas8v98171': {'firstSeen': 1534382478, 'lastSeen': 1534382478}},
                         generator.user_summary)
        generator.createDataSummary('{userId}', '1234')
        self.assertEqual(generator.invalid_user_data[0], '1234')

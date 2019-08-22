import unittest
from unittest.mock import patch, Mock

from app.src.data.detail_data_generator import DetailDataGenerator


class TestDetailsDataGenerator(unittest.TestCase):
    def test_publish_raw_data(self):
        client = Mock()
        client.send_data.return_value = None
        generator = DetailDataGenerator(client, 'some_topic')
        generator.publish_raw_data(1)
        self.assertEqual(1, generator.kafka_client.send_data.call_count)

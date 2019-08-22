import json
import unittest

from app.src.util.summary_utils import validate_json, read_config


class TestSummaryUtils(unittest.TestCase):
    def test_validate_json_for_valid_data(self):
        valid_data = {
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
        }

        isvalid = validate_json(json.loads(json.dumps(valid_data)), 'visitor_schema')
        self.assertTrue(isvalid)

        invalid_data = {
            "userId": "jas8v98171",
            "visitorId": "jas8v98171"
        }
        isvalid = validate_json(json.loads(json.dumps(invalid_data)), 'visitor_schema')
        self.assertFalse(isvalid)

    def test_read_config(self):
        self.assertRaises(Exception, read_config, 'someconfig')
        config = read_config('application_config_dev.yaml')
        self.assertIsNotNone(config)

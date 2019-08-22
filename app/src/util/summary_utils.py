import json
import logging
import os

import yaml
from jsonschema import validate, ValidationError

dir_path = os.path.dirname(os.path.realpath(__file__))
schema_path = dir_path + '\\..\\config\\'


def validate_json(input, schmea):
    is_valid = True
    try:
        with open(schema_path + schmea) as json_file:
            json_load = json.load(json_file)
            validate(input, json_load)
    except ValidationError as err:
        logging.error(err)
        is_valid = False
    return is_valid


def read_config(config_name):
    try:
        with open(schema_path + config_name) as ymlfile:
            conf = yaml.safe_load(ymlfile)
            conf['kafka']['connection']['ssl.ca.location'] = schema_path + 'cloudkarafka.ca'
            return conf
    except Exception as e:
        logging.info("Cant read the Configuration file %s" % config_name)
        raise e

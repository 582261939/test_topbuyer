import os
from configparser import ConfigParser
from common.get_path import CONFIG_PATH


def get_config(file_path):
    config = ConfigParser()
    config.read(file_path)
    return config


config_data = get_config(os.path.join(CONFIG_PATH, "config.ini"))
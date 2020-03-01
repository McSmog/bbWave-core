import os
import sys
import logging
import configparser

# config_path = '/etc/bbwave/core/config.ini'
config_path = '{}/{}'.format(os.getcwd(), 'bbWave-core/config.ini')


def get_configuration():
    if not os.path.exists(config_path):
        logging.error('Config not found!')
        sys.exit(-1)

    config = configparser.ConfigParser()
    config.read(config_path)
    return config

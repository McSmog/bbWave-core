import os
import sys
import logging
import configparser

# config_path = '/etc/bbwave/core/config.ini'
config_path = '{}/{}'.format(os.getcwd(), 'config.ini')


def get_configuration(path=config_path):
    if not os.path.exists(path):
        logging.error('Config "{}" not found!'.format(path))
        sys.exit(-1)

    config = configparser.ConfigParser()
    config.read(path)
    return config

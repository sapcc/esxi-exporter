from modules.Globals import Globals

from importlib import import_module
from time import sleep
from prometheus_client import REGISTRY, start_http_server

import logging

logger = logging.getLogger('esxi')


def init_logger():
    global_config = Globals()
    if global_config.info:
        logger.setLevel(logging.INFO)
    if global_config.debug:
        logger.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def init_collectors():
    global_config = Globals()

    collectors = []

    for entry in global_config.collectors.__dict__.keys():
        try:
            class_name = ''.join([part[0].upper() + part[1:] for part in entry.split('_')])
            class_module = import_module(f'collectors.{class_name}')
        except ModuleNotFoundError as ex:
            logger.error('Module not found: %s -> %s. Ignoring...' % (entry,class_name))
            continue

        try:
            collectors.append(class_module.__getattribute__(class_name)())
        except AttributeError as ex:
            logger.error('Class not found: %s. Ignoring...' % (str(class_module)))

    return collectors


if __name__ == '__main__':
    init_logger()
    global_config = Globals()

    logger.debug('starting http server...')
    start_http_server(global_config.port)

    collectors = init_collectors()
    for collector in collectors:
        logger.debug('Registering %s' % collector.__module__)
        REGISTRY.register(collector)

    logger.info('exporter is ready')
    while True:
        sleep(1)
from modules.configuration.Configuration import Configuration

from importlib import import_module
from time import sleep
from prometheus_client import REGISTRY, start_http_server

import logging

logger = logging.getLogger('esxi')


def init_logger(logging_mode):
    logger.setLevel(logging_mode)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def get_collector(collector_name):
    class_module = import_module(f'collectors.{collector_name}')
    return class_module.__getattribute__(collector_name)


def init_collectors(config: Configuration):
    collectors = list()

    if config.enable_critical_serivce_collector:
        collectors.append(get_collector('CriticalServiceCollector')(config))
    if config.enable_overall_status_collector:
        collectors.append(get_collector('OverallStateCollector')(config))

    return collectors


if __name__ == '__main__':
    config = Configuration()

    init_logger(config.logging_mode)

    logger.debug('starting http server...')
    start_http_server(config.port)

    collectors = init_collectors(config)
    for collector in collectors:
        logger.debug('Registering %s' % collector.__module__)
        REGISTRY.register(collector)

    logger.info('exporter is ready')
    while True:
        sleep(1)

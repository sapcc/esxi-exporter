from BaseCollector import BaseCollector
from modules.configuration.ExporterConfig import ExporterConfig

from prometheus_client import REGISTRY, start_http_server

from importlib import import_module
from time import sleep
from typing import List

import logging

logger = logging.getLogger('esxi')


def init_logger(logging_mode):
    """
    Setup logger format and output
    """
    logger.setLevel(logging_mode)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def import_collector(collector_name) -> BaseCollector:
    """
    Imports collectors from collectors folder.

    :param collector_name: The name of the collector. The filename must be equal to the class name.
    :return: a uninitialized super class of BaseCollector.
    """
    class_module = import_module(f'collectors.{collector_name}')
    return class_module.__getattribute__(collector_name)


def get_enabled_collectors(config: ExporterConfig) -> List[BaseCollector]:
    """
    Returns a list of uninitialized collector classes

    :type config: A config containing information about the collectors to be activated.
    :return: A list of uninitialized collectors.
    """

    collectors = list()

    if config.enable_cricital_service_collector:
        collectors.append(import_collector('CriticalServiceCollector'))
    if config.enable_overall_state_collector:
        collectors.append(import_collector('OverallStateCollector'))

    return collectors


if __name__ == '__main__':

    config = ExporterConfig()
    init_logger(config.logging_mode)

    logger.debug('starting http server...')
    start_http_server(int(config.port))

    collectors = get_enabled_collectors(config)
    for collector in collectors:
        logger.debug('Registering %s' % collector.__module__)
        REGISTRY.register(collector())

    logger.info('exporter is ready')
    while True:
        sleep(1)

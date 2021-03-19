from modules.Globals import Globals
from collectors.CriticalServiceCollector import CriticalServiceCollector
from collectors.OverallStateCollector import OverallStateCollector

from time import sleep
from prometheus_client import REGISTRY, start_http_server
import logging

logger = logging.getLogger('esxi')


def init_logger():
    global_config = Globals()
    if global_config.debug:
        logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

if __name__ == '__main__':
    init_logger()
    global_config = Globals()

    logger.debug('starting http server...')
    start_http_server(global_config.port)
    REGISTRY.register(CriticalServiceCollector())
    REGISTRY.register(OverallStateCollector())
    logger.info('exporter is ready')
    while True:
        sleep(1)
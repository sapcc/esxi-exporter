import logging
import os
import time
from os import getenv

import urllib3
from prometheus_client import REGISTRY, start_http_server

from collectors.EsxiOverallStateCollector import EsxiOnlineStateCollector
from collectors.PyVimServiceCollector import PyVimServiceCollector
from collectors.SshServiceCollector import SshServiceCollector
import modules.Configuration as config

# disable ssl warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# init logger once
logger = logging.getLogger('esxi-exporter')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def run_prometheus_server(port: int) -> None:
    """
    Starts a prometheus server which will stay running
    :param port: The port the server should listen on
    """

    # startup prometheus server
    logger.info("starting http server...")
    start_http_server(port)

    # register collectors
    if config.enable_pyvim:
        logger.info("registering collector: PyVimServiceCollector... ")
        REGISTRY.register(PyVimServiceCollector())
    if config.enable_ssh:
        logger.info("registering collector: sshServiceCollector...")
        REGISTRY.register(SshServiceCollector())
    if config.enable_overall_state:
        logger.info("registering collector: EsxiOverallStateCollector...")
        REGISTRY.register(EsxiOnlineStateCollector())

    logger.info("exporter is ready")

    while True:
        time.sleep(1)


def check_env_vars():
    logger.info('checking environment variables...')
    str_env = ('VCENTER_USER', 'VCENTER_PASSWORD',
               'VCENTER_URL', 'ESXI_PASSWORD', 'NETBOX_URL')
    for item in str_env:
        if os.getenv(item) is None:
            logger.critical(
                'A environment variable of type string is missing: %s' % item)
            exit(0)

    logger.info('All environment variables are set.')


if __name__ == '__main__':
    check_env_vars()
    try:
        run_prometheus_server(config.port)
    except Exception as ex:
        logger.critical(ex)
        raise ex

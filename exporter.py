import logging
import time
from os import getenv

import os

import urllib3
from prometheus_client import REGISTRY, start_http_server

from collectors.PyVimServiceCollector import PyVimServiceCollector
from collectors.SshServiceCollector import SshServiceCollector
from collectors.EsxiOverallStateCollector import EsxiOnlineStateCollector
from modules.Exceptions import VCenterException

# init logger once
logger = logging.getLogger('esxi-exporter')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# disable ssl warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Exporter:

    def __init__(self) -> None:
        self.check_config()
        try:
            self.run_prometheus_server(int(getenv('EXPORTER_PORT', 1234)))
        except Exception as ex:
            logger.critical(ex)
            raise ex

    @staticmethod
    def run_prometheus_server(port: int) -> None:
        """
        Starts a prometheus server which will stay running
        :param port: The port the server should listen on
        """

        # startup prometheus server
        logger.info("starting http server...")
        start_http_server(port)

        # register collectors
        if not bool(getenv('DISABLE_PYVIM', False)):
            logger.info("registering collector: PyVimServiceCollector... ")
            REGISTRY.register(PyVimServiceCollector())
        if not bool(getenv('DISABLE_SSH', False)):
            logger.info("registering collector: sshServiceCollector...")
            REGISTRY.register(SshServiceCollector())
        if not bool(getenv('DISABLE_OVERALLSTATE', False)):
            logger.info("registering collector: EsxiOverallStateCollector...")
            REGISTRY.register(EsxiOnlineStateCollector())

        logger.info("exporter is ready")

        while True:
            time.sleep(1)

    @staticmethod
    def check_config():
        # Optional: 'esxi_user', 'PORT', 'CASHTIME', 'BLACKLISTTIME
        logger.info('checking configuration...')
        str_env = ('VCENTER_USER', 'VCENTER_PASSWORD',
                   'VCENTER_URL', 'ESXI_PASSWORD', 'NETBOX_URL')
        for item in str_env:
            if os.getenv(item) == None:
                logger.critical(
                    'A environment variable of type string is missing: %s' % item)
                exit(0)

        int_env = ('PORT', 'CASHTIME', 'BLACKLISTTIME',
                   'SSH_WORKERCOUNT', 'VC_WORKERCOUNT')
        for item in int_env:
            try:
                if os.getenv(item) != None and not isinstance(int(os.getenv(item)), int):
                    logger.critical(
                        'The environment variable is not instance of int: %s' % item)
                    exit(0)
            except TypeError:
                logger.critical(
                    'The environment variable is not instance of int: %s' % item)
                exit(0)

        bool_env = ('DISABLE_PYVIM', 'DISABLE_SSH', 'DISABLE_OVERALLSTATE')
        for item in int_env:
            try:
                if os.getenv(item) != None and not isinstance(bool(os.getenv(item)), bool):
                    logger.critical(
                        'The environment variable is not instance of boolean: %s' % item)
                    exit(0)
            except TypeError:
                logger.critical(
                    'The environment variable is not instance of boolean: %s' % item)
                exit(0)

        logger.info('configuration tests passed')



if __name__ == '__main__':
    Exporter()
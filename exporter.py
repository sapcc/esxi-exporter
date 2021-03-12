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
logger = logger = logging.getLogger('esxi-exporter')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# disable ssl warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Exporter:

    def run_prometheus_server(self, port: int) -> None:
        """
        Starts a prometheus server which will stay running
        :param port: The port the server should listen on
        """

        # startup prometheus server
        logger.info("starting http server...")
        start_http_server(port)

        # register collectors
        if not bool(getenv('disable_pyvim', False)):
            logger.info("registering collector: PyVimServiceCollector... ")
            REGISTRY.register(PyVimServiceCollector())
        if not bool(getenv('disable_ssh', False)):
            logger.info("registering collector: sshServiceCollector...")
            REGISTRY.register(SshServiceCollector())
        if not bool(getenv('disable_overallstate', False)):
            logger.info("registering collector: EsxiOverallStateCollector...")
            REGISTRY.register(EsxiOnlineStateCollector())

        logger.info("exporter is ready")

        # stay alive
        while True:
            time.sleep(1)

    def run(self):
        try:
            self.run_prometheus_server(int(getenv('exporter_port', 1234)))
        except Exception as ex:
            logger.critical(ex)
            raise ex

    def check_config(self):
        # Optional: 'esxi_user', 'port', 'cashtime', 'blacklisttime
        logger.info('checking configuration...')
        str_env = ('vcenter_user', 'vcenter_password',
                   'vcenter_url', 'esxi_password', 'netbox_url')
        for item in str_env:
            if os.getenv(item) == None:
                logger.critical(
                    'A environment variable of type string is missing: %s' % item)
                exit(0)

        int_env = ('port', 'cashtime', 'blacklisttime',
                   'ssh_workercount', 'vc_workercount')
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

        bool_env = ('disable_pyvim', 'disable_ssh', 'disable_overallstate')
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
    exporter = Exporter()
    exporter.check_config()
    exporter.run()

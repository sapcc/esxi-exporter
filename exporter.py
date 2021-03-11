import logging
import time
from os import getenv

import os

import urllib3
from prometheus_client import REGISTRY, start_http_server

from collectors.PyVimServiceCollector import PyVimServiceCollector
from collectors.SshServiceCollector import SshServiceCollector
from collectors.EsxiOverallStateCollector import  EsxiOnlineStateCollector
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
        logger.info("registering collector: EsxiOverallStateCollector...")
        REGISTRY.register(EsxiOnlineStateCollector())

        logger.info("exporter is ready")

        # stay alive
        while True:
            time.sleep(1)

    def run(self):
            try:
                self.run_prometheus_server(int(getenv('exporter_port', 1234)))

            except VCenterException:
                logger.error("vCenter error occurred. Trying to restart application.")

            except Exception as ex:
                logger.critical(ex)
                raise ex

if __name__ == '__main__':
    Exporter().run()

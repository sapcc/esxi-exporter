import logging
from modules.Exceptions import VCenterException
import time
import urllib3

from prometheus_client import REGISTRY, start_http_server

from collectors.PyVimServiceCollector import PyVimServiceCollector
from collectors.SshServiceCollector import SshServiceCollector

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

import modules.Configuration as config 

# disable ssl warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Exporter:

    def __init__(self):
        # load config
        self.successful_start: bool = False

    def run_prometheus_server(self, port: int) -> None:
        """
        Starts a prometheus server which will stay running
        :param port: The port the server should listen on
        """

        # startup prometheus server
        logger.info("starting http server...")
        start_http_server(port)

        # register collectors
        if not config.pyVimDisable:
            logger.info("registering collector: PyVimServiceCollector... ")
            REGISTRY.register(PyVimServiceCollector())
        if not config.sshDisable:
            logger.info("registering collector: sshServiceCollector...")
            REGISTRY.register(SshServiceCollector())
        logger.info("exporter is ready")

        # there was a succesful start
        # so there is a working config and the app can try to restart
        # if it looses its connection
        self.successful_start = True

        # stay alive
        while True:
            time.sleep(1)

    def run(self):
        # try to restart if there was at least one successful start
        # eg if the vCenter is not reachable but goes online later again
        # this container will automatically reconnect
        while True:
            # todo: catch critical exceptions and not critical exceptions
            try:
                self.run_prometheus_server(config.port)

            except VCenterException:
                logger.error("vCenter error occurred. Trying to restart application.")
                if not self.successful_start:
                    exit(0)
                time.sleep(180)
                continue

            except Exception as ex:
                logger.critical(ex)
                raise ex

if __name__ == '__main__':
    Exporter().run()

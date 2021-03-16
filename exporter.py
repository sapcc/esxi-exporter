from optparse import OptionParser
from prometheus_client import REGISTRY, start_http_server

import importlib
import logging
import os
import time
import urllib3
import modules.Configuration as config

# disable ssl warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# init logger once
logger = logging.getLogger('esxi-exporter')
parser = OptionParser()
parser.add_option("-d", "--debug", dest="debug", help="enable debug output",
                  action="store_true")
parser.add_option("-v", "--info", dest="info", help="enable info output",
                  action="store_true")
(options, args) = parser.parse_args()
if options.debug:
    logger.setLevel(logging.DEBUG)
elif options.info:
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.WARNING)
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
    logger.debug("starting http server...")
    start_http_server(port)

    for collector in get_collectors():
        logger.debug(
            f"registering collector: {collector.__name__.split('.')[-1]}")
        REGISTRY.register(collector())

    logger.info("exporter is ready")

    while True:
        time.sleep(1)


# https://github.com/sapcc/vrops-exporter/blob/master/exporter.py#L92-L105
def get_collectors() -> list:
    """
    Get all collectors which are named in config.yaml > collectors section

    :return: list of BaseCollector classes
    """

    results = []
    for collector_name in config.collectors:
        try:
            class_module = importlib.import_module(
                f'collectors.{collector_name}')
        except ModuleNotFoundError as ex:
            logger.error(f'No module {collector_name} defined. {ex}')
            return None

        try:
            results.append(class_module.__getattribute__(collector_name))
        except AttributeError as ex:
            logger.error(f'Unable to get class {collector_name}. {ex}')
            return None
    return results


def check_env_vars():
    logger.debug('checking environment variables...')
    str_env = (
        'VCENTER_USER', 'VCENTER_PASSWORD', 'VCENTER_URL', 'ESXI_PASSWORD',
        'NETBOX_URL')
    for item in str_env:
        if os.getenv(item) is None:
            logger.critical(
                'A environment variable of type string is missing: %s' % item)
            exit(0)

    logger.debug('All environment variables are set.')


if __name__ == '__main__':
    check_env_vars()
    try:
        run_prometheus_server(config.port)
    except Exception as ex:
        logger.critical(ex)
        raise ex

import logging

from prometheus_client.core import GaugeMetricFamily

from BaseCollector import BaseCollector
from modules.VCenterConnection import VCenterConnection

import modules.Configuration as config

# init logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class PyVimServiceCollector(BaseCollector):

    def __init__(self):
        """
        :param config: the configuration which provides credentials etc.
        """

        config = config
        logger.info('connecting to vcenter: ' + config.vCenter)
        self._conn = VCenterConnection(config.vCenter, config.vCenter_username, config.vCenter_password)

    def collect(self):
        """
        Collects information about critical esxi host services
        To be registered at a prometheus http server
        :return: yield GaugeMetricFamily
        """

        gauge_metric = GaugeMetricFamily('esxi_pyvim_service_state', '1=running, 0=stopped',
                                         labels=['vcenter', 'host', 'service'])

        if not self._conn.is_alive():
            self._conn = VCenterConnection(config.vCenter, config.vCenter_username,
                                           config.vCenter_password)

        # get esxi hosts from vCenter
        hosts = self._conn.get_hosts()
        for host in hosts:
            services = host.configManager.serviceSystem.serviceInfo.service
            for service in services:
                gauge_metric.add_metric(labels=[config.vCenter, host.name, service.key], value=service.running)

        yield gauge_metric

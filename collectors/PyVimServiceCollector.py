import logging
from os import getenv

from prometheus_client.core import GaugeMetricFamily

from BaseCollector import BaseCollector

# init logging
logger = logging.getLogger('esxi-exporter')


class PyVimServiceCollector(BaseCollector):

    def __init__(self) -> None:
        super().__init__()

    def collect(self):
        """
        Collects information about critical esxi host services
        To be registered at a prometheus http server
        :return: yield GaugeMetricFamily
        """

        gauge_metric = GaugeMetricFamily('esxi_pyvim_service_state', '1=running, 0=stopped',
                                         labels=['vcenter', 'hostsystem', 'service'])

        # get esxi hosts from vCenter
        hosts = self.get_active_hosts()
        for host in hosts:
            services = host.configManager.serviceSystem.serviceInfo.service
            for service in services:
                gauge_metric.add_metric(labels=[getenv('vcenter_url'), host.name, service.key], value=service.running)

        yield gauge_metric

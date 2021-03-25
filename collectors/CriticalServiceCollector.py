from prometheus_client.core import GaugeMetricFamily
from BaseCollector import BaseCollector
from modules.configuration.CriticalServiceCollectorConfig import CriticalServiceCollectorConfig
from modules.helper.EsxiServiceHelper import EsxiServiceHelper


class CriticalServiceCollector(BaseCollector):

    def __init__(self):
        super(CriticalServiceCollector, self).__init__()
        config = CriticalServiceCollectorConfig()
        self.esxi_helper = EsxiServiceHelper(self.atlas, config.esxi_username, config.esxi_password, config.critical_services,
                                             config.max_threads)

    def describe(self):
        """
        Descripe is used to prevent calling collect() method at program startup.
        So only a description from describe() will be invoked.
        """
        yield GaugeMetricFamily(
            'esxi_critical_service_status',
            'running=1/stopped=0',
            labels=['site', 'hostsystem', 'service'])

    def collect(self):
        """
        Collects all information about critical services at listed esxi-hosts and returns them as metic.
        """
        metric = GaugeMetricFamily('esxi_critical_service_status', 'running=1/stopped=0',
                                   labels=['site', 'hostsystem', 'service'])

        hosts = self.esxi_helper.get_all_service_stats()
        for host in hosts:
            for service, state in host.services.items():
                metric.add_metric([host.site, host.address, service], state)

        yield metric

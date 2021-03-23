from prometheus_client.core import GaugeMetricFamily
from BaseCollector import BaseCollector


class CriticalServiceCollector(BaseCollector):

    def describe(self):
        metric = GaugeMetricFamily(
            'esxi_critical_service_status',
            'running=1/stopped=0',
            labels=['site', 'hostsystem', 'service'])

        yield metric

    def collect(self):
        metric = GaugeMetricFamily('esxi_critical_service_status', 'running=1/stopped=0',
                                   labels=['site', 'hostsystem', 'service'])

        hosts = self.get_host_service_stats()
        for host in hosts:
            for service, state in host.services.items():
                    metric.add_metric([host.site, host.address, service], state)

        yield metric

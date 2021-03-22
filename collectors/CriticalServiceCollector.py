from prometheus_client.core import GaugeMetricFamily
from BaseCollector import BaseCollector


class CriticalServiceCollector(BaseCollector):

    def describe(self):
        metric = GaugeMetricFamily(
            'esxi_critical_service_status',
            'running=1/stopped=0',
            labels=['vcenter', 'host', 'service'])

        yield metric

    def collect(self):
        metric = GaugeMetricFamily('esxi_critical_service_status', 'running=1/stopped=0',
                                   labels=['vcenter', 'host', 'service'])

        hosts = self.get_host_service_stats()
        for host in hosts:
            for service, state in host.services.items():
                if host.vcenter is not None:
                    metric.add_metric([host.vcenter.name, host.address, service], state)
                else:
                    metric.add_metric(['undefined', host.address, service], state)

        yield metric

from prometheus_client.core import GaugeMetricFamily

from BaseCollector import BaseCollector


class OverallStateCollector(BaseCollector):

    def describe(self):
        metric = GaugeMetricFamily('esxi_overall_status', 'green=2/yellow=1/red=0',
                                   labels=['vcenter', 'hostsystem'])
        yield metric

    def collect(self):

        metric = GaugeMetricFamily('esxi_overall_status', 'green=2/yellow=1/red=0',
                                   labels=['vcenter', 'hostsystem'])

        esxi_stats = self.get_host_overall_stats()

        if esxi_stats is not None:
            for host in esxi_stats:
                metric.add_metric([host.vcenter.name, host.name], host.overall_status)

        yield metric

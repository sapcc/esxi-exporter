from prometheus_client.core import GaugeMetricFamily
from BaseCollector import BaseCollector
from modules.configuration.OverallStateCollectorConfig import OverallStateCollectorConfig
from modules.helper.VCenterHelper import VCenterHelper


class OverallStateCollector(BaseCollector):

    def __init__(self):
        config = OverallStateCollectorConfig()
        self.vcenter_helper = VCenterHelper(config.vcenter_username, config.vcenter_password)

    def describe(self):
        """
        Descripe is used to prevent calling collect() method at program startup.
        So only a description from describe() will be invoked.
        """
        metric = GaugeMetricFamily('esxi_overall_status', 'green=2/yellow=1/red=0',
                                   labels=['vcenter', 'hostsystem'])
        yield metric

    def collect(self):
        """
        Collects the overall-state of esxi-hosts as displayed in vcenter-mob and returns them as metic.
        Vcenter-mob refers to its managed-object-browser.
        """
        metric = GaugeMetricFamily('esxi_overall_status', 'green=2/yellow=1/red=0',
                                   labels=['vcenter', 'hostsystem'])

        esxi_stats = self.vcenter_helper.get_esxi_overall_stats()

        if esxi_stats is not None:
            for host in esxi_stats:
                metric.add_metric([host.vcenter.name, host.name], host.overall_status)

        yield metric

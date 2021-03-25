from prometheus_client.core import GaugeMetricFamily
from BaseCollector import BaseCollector
from modules.configuration.OverallStateCollectorConfig import OverallStateCollectorConfig
from modules.helper.VCenterHelper import VCenterHelper


class OverallStateCollector(BaseCollector):

    def __init__(self):
        super(OverallStateCollector, self).__init__()
        config = OverallStateCollectorConfig()
        self.vcenter_helper = VCenterHelper(self.atlas, config.vcenter_username, config.vcenter_password, self.verify_ssl)

    def describe(self):
        """
        Descripe is used to prevent calling collect() method at program startup.
        So only a description from describe() will be invoked.
        """
        yield GaugeMetricFamily('esxi_overall_status', 'green=2/yellow=1/red=0',
                                labels=['vcenter', 'site', 'hostsystem'])

    def collect(self):
        """
        Collects the overall-state of esxi-hosts as displayed in vcenter-mob and returns them as metic.
        Vcenter-mob refers to its managed-object-browser.
        """
        metric = GaugeMetricFamily('esxi_overall_status', 'green=2/yellow=1/red=0',
                                   labels=['vcenter', 'site', 'hostsystem'])

        for host in self.vcenter_helper.get_esxi_overall_stats_for_all_vcenters():
            metric.add_metric([host.vcenter.name, host.site, host.name], host.overall_status)

        yield metric

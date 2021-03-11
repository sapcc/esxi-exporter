import datetime
import logging
from os import getenv

from prometheus_client.core import GaugeMetricFamily

from BaseCollector import BaseCollector

# init logging
logger = logging.getLogger('esxi-exporter')


class EsxiOnlineStateCollector(BaseCollector):

    def __init__(self) -> None:
        super().__init__()

    def collect(self):
        starttime = datetime.datetime.now()

        gauge_metric = GaugeMetricFamily('esxi_overall_state', '0=unknown 1=red, 2=orange, 3=green',
                                         labels=['vcenter', 'hostsystem'])

        # get all hosts from vcenter
        vc_hosts = self.get_vcenter_hosts()
        for host in vc_hosts:
            if host.overallStatus == 'green':
                state = 3
            elif host.overallStatus == 'orange':
                state = 2
            elif host.overallStatus == 'red':
                state = 1
            else:
                state = 0
            gauge_metric.add_metric(labels=[getenv('vcenter_url'), host.name, 'ssh_connection'], value=state)

        print((datetime.datetime.now() - starttime))

        yield gauge_metric

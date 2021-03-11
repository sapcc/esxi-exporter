import datetime
import logging
from os import getenv

from prometheus_client.core import GaugeMetricFamily

import modules.TimedBlacklist as blacklist
from BaseCollector import BaseCollector

# init logging
logger = logging.getLogger('esxi-exporter')


class EsxiOnlineStateCollector(BaseCollector):

    def __init__(self) -> None:
        super().__init__()

    def collect(self):
        starttime = datetime.datetime.now()

        gauge_metric = GaugeMetricFamily('esxi_online_state', '1=online, 0=offline',
                                         labels=['vcenter', 'host', 'origin'])

        # get all hosts from vcenter
        vc_hosts = self.get_vcenter_hosts()
        for host in vc_hosts:
            nb_state = self.netbox.is_host_active(host.name.split('.')[0])
            gauge_metric.add_metric(labels=[getenv('vcenter_url'), host.name, 'netbox'], value=nb_state)

            bl_state = blacklist.is_host_allowed(host.name)
            gauge_metric.add_metric(labels=[getenv('vcenter_url'), host.name, 'ssh_connection'], value=bl_state)

        print((datetime.datetime.now() - starttime))

        yield gauge_metric

import logging
from abc import ABC, abstractmethod
from os import getenv

import modules.TimedBlacklist as blacklist
from modules.NetboxHelper import NetboxHelper
from modules.VCenterConnection import VCenterConnection

logger = logging.getLogger('esxi-exporter')


class BaseCollector(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.vCenter = VCenterConnection(getenv('VCENTER_URL'), getenv('VCENTER_USER'), getenv('VCENTER_PASSWORD'))
        self.netbox = NetboxHelper()

    @abstractmethod
    def collect(self):
        pass

    def _check_connection(self) -> None:
        if not self.vCenter.is_alive():
            self.vCenter = VCenterConnection(getenv('VCENTER_URL'), getenv('VCENTER_USER'), getenv('VCENTER_PASSWORD'))

    def get_active_hosts(self) -> list:
        self._check_connection()

        hosts = self.vCenter.get_hosts()
        hosts = [host for host in hosts if
                 self.netbox.is_host_active(host.name.split('.')[0]) and blacklist.is_host_allowed(host.name)]
        logger.info('%i active hosts at %s' % (len(hosts), getenv('VCENTER_URL')))
        return hosts

    def get_vcenter_hosts(self) -> list:
        self._check_connection()
        hosts = self.vCenter.get_hosts()
        return hosts

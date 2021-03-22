from modules.helper.VCenterHelper import VCenterHelper
from interfaces.vcenter import Vcenter
from modules.Globals import Globals
from modules.api.Atlas import Atlas
from modules.api.VcenterConnection import VcenterConnection
from modules.helper.EsxiServiceHelper import EsxiServiceHelper


class UnifiedInterface():

    def __init__(self) -> None:
        self.globals = Globals()
        self.atlas = Atlas()
        self.esxi_helper = EsxiServiceHelper()
        self.vcenter_helper = VCenterHelper()

    def get_hosts_by_vcenter(self, vcenter: Vcenter) -> list:
        return self.netbox.get_hosts_by_vcenter(vcenter)

    def get_vcenters(self) -> list:
        return self.atlas.get_vcenters()

    def get_host_service_stats(self) -> list:
        return self.esxi_helper.get_all_service_stats()

    def get_host_overall_stats(self) -> list:
        return self.vcenter_helper.get_esxi_overall_stats()

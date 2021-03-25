from interfaces.host import Host
from modules.api.Atlas import Atlas
from modules.api.VcenterConnection import VcenterConnection

from typing import List


class VCenterHelper:

    def __init__(self, atlas: Atlas, vcenter_username: str, vcenter_password, verify_ssl=False):
        self.atlas = atlas
        self.vcenter_username = vcenter_username
        self.vcenter_password = vcenter_password
        self.verify_ssl = verify_ssl

    def get_esxi_overall_stats_for_all_vcenters(self) -> List[Host]:
        """
        Collects the overall state of esxi-hosts as displayed in the vcenter.

        :return: List of Host
        """

        results = list()
        for vcenter in self.atlas.get_vcenters():
            vc_conn = VcenterConnection(
                vcenter.address,
                self.vcenter_username,
                self.vcenter_password,
                self.verify_ssl
            )

            results.extend(vc_conn.get_esxi_overall_stats())

        return results

from interfaces.host import Host
from modules.helper.GeneralHelper import GeneralHelper
from modules.api.VcenterConnection import VcenterConnection

from typing import List


class VCenterHelper:

    def __init__(self, vcenter_username: str, vcenter_password) -> None:
        self.general_helper = GeneralHelper()
        self.vcenter_username = vcenter_username
        self.vcenter_password = vcenter_password

    def get_esxi_overall_stats(self) -> List[Host]:
        """
        Collects the overall state of esxi-hosts as displayed in the vcenter.

        :return: List of Host
        """

        results = []
        for vcenter in self.general_helper.get_vcenters():
            vc_conn = VcenterConnection(
                vcenter.address,
                self.vcenter_username,
                self.vcenter_password
            )
            results.extend(vc_conn.get_esxi_overall_stats())

        return results

from modules.Globals import Globals
from modules.api.Atlas import Atlas
from modules.api.VcenterConnection import VcenterConnection


class VCenterHelper:

    def __init__(self) -> None:
        self.globals = Globals()
        self.atlas = Atlas()

    def get_esxi_overall_stats(self):
        results = []
        for vcenter in self.atlas.get_vcenters():
            vc_conn = VcenterConnection(
                vcenter.address,
                self.globals.vcenter_user,
                self.globals.vcenter_password
            )
            results.extend(vc_conn.get_esxi_overall_stats())

        return results

from modules.api.Atlas import Atlas
from modules.api.VcenterConnection import VcenterConnection
from modules.configuration.Configuration import Configuration


class VCenterHelper:

    def __init__(self, config: Configuration) -> None:
        self.config = config
        self.atlas = Atlas(config)

    def get_esxi_overall_stats(self):
        results = []
        for vcenter in self.atlas.get_vcenters():
            vc_conn = VcenterConnection(
                vcenter.address,
                self.config.vcenter_user,
                self.config.vcenter_password
            )
            results.extend(vc_conn.get_esxi_overall_stats())

        return results

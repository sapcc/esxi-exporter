from interfaces.host import Host
from interfaces.vcenter import Vcenter
from modules.configuration.GeneralHelperConfig import GeneralHelperConfig
from modules.api.Atlas import Atlas

from typing import List


class GeneralHelper:
    """
    The general helper provides functionality of shared APIs.
    """

    def __init__(self):
        config = GeneralHelperConfig()
        self.atlas = Atlas(config.atlas_file)

    def get_vcenters(self) -> List[Vcenter]:
        return self.atlas.get_vcenters()

    def get_esxi_hosts(self) -> List[Host]:
        return self.atlas.get_esxi_hosts()

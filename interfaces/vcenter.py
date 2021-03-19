class Vcenter:

    def __init__(self, name: str, address: str, site=None) -> None:
        """
        Represents a vcenter

        :param name: The name of the vcenter. Same as address
        :param address: The address of the vcenter. Use url format only.
        :param site: the site / region where the vcenter is located
        """
        self.name = name
        self.address = address
        self.site = site

    @property
    def region(self) -> str:
        # node.cc.region.cloud.sap
        return self.name.split('.')[2]
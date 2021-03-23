class Vcenter:

    def __init__(self, name: str, address: str) -> None:
        """
        Represents a vcenter

        :param name: The name of the vcenter. Same as address
        :param address: The address of the vcenter. Use url format only.
        :param site: the site / region where the vcenter is located
        """
        self.name = name
        self.address = address

    @property
    def region(self) -> str:
        # node.cc.region.cloud.sap
        return self.name.split('.')[2]

    @property
    def site(self) -> str:
        # vc-x-0.cc.region.cloud.sap
        segments = self.name.split('.')
        site = segments[0].split('-')[1]
        region = segments[2]
        return region + site

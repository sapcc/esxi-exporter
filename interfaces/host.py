from interfaces.vcenter import Vcenter


class Host:

    def __init__(self, name: str, address: str, site=None, vcenter: Vcenter = None, server_state: str = None,
                 overall_status: str = None):
        """
        Represents a ESXi HostSystem

        :param name: The name of the host
        :param address: The url to the host. Please use url.
        :param site: The site / region of the host.
        :param vcenter: The vcenter of the region
        :param server_state: The netbox / atlas status of this host
        :param overall_status: The vcenter overall_status of this host
        """

        self.name: str = name
        self.address: str = address
        self.server_state: str = server_state
        self.overall_status = overall_status
        self.site: str = site
        self.vcenter: Vcenter = vcenter
        self.services: dict = None

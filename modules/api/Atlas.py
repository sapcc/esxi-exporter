from modules.Singleton import Singleton
from modules.Globals import Globals
from interfaces.host import Host  
from interfaces.vcenter import Vcenter  

import json

class Atlas(metaclass=Singleton):
    def __init__(self) -> None:
        self.globals = Globals()


    def load_file(self):
        """
        Loads the atlas.json and returns its content

        :return: atlas.json as dict.
        """

        with open(self.globals.ATLAS_FILE, 'rt', encoding='utf8') as f:
            data = json.load(f)
        return data

    def get_vcenters(self) -> list:
        """
        Get all vcenters. Returns a list of Vcenter

        :return: list of Vcenter
        """

        results = []
        for target in self.load_file():
            if target['labels']['job'] == 'vcenter':
                results.append(Vcenter(
                    name = target['labels']['server_name'],
                    address = target['targets'][0]))
        return results

    def get_esxi_hosts(self) -> list:
        """
        Get all esxi-hosts. Returns a list of Host

        :return: list of Host
        """

        results = []
        for target in self.load_file():
            if target['labels']['job'] == 'vmware-esxi':
                results.append(Host(
                    name = target['labels']['server_name'],
                    address = target['targets'][0]))
        return results
from modules.Exceptions import AtlasError
from modules.Singleton import Singleton
from modules.Globals import Globals
from interfaces.host import Host
from interfaces.vcenter import Vcenter

import json
import re
import logging


logger = logging.getLogger('esxi')


class Atlas(metaclass=Singleton):
    def __init__(self) -> None:
        self.globals = Globals()
        self.re_site = re.compile(r'([A-Z]{2}\-[A-Z]{2}\-[0-9])[a-z]', re.IGNORECASE)

    def load_file(self):
        """
        Loads the atlas.json and returns its content

        :return: atlas.json as dict.
        """

        logger.debug('Opening atlas file: %s' % self.globals.atlas_file)

        try:
            with open(self.globals.atlas_file, 'rt', encoding='utf8') as f:
                data = json.load(f)
            return data
        except IOError as ex:
            raise AtlasError('could not open atlas file: %s ' % self.globals.atlas_file) from ex

    def get_vcenters(self) -> list:
        """
        Get all vcenters.

        :return: list of interfaces.Vcenter
        """

        logger.debug('getting vcenters from atlas...')

        results = []
        for target in self.load_file():
            if target['labels']['job'] == 'vcenter':
                results.append(Vcenter(
                    name=target['labels']['server_name'],
                    address=target['labels']['server_name'],
                    )
                )
        return results

    def get_esxi_hosts(self) -> list:
        """
        Get all esxi-hosts. Returns a list of Host

        :return: list of Host
        """

        logger.debug('getting esxi-hosts from atlas...')

        results = []
        vcenters = self.get_vcenters()

        for target in self.load_file():
            if target['labels']['job'] == 'vmware-esxi':
                name = target['labels']['name']
                site = target['labels']['site']
                region = self.re_site.match(site).group(1)
                status = target['labels']['status']
                url = f'{name}.cc.{region}.cloud.sap'
                vcenter = [
                    vcenter for vcenter in vcenters if vcenter.site == site]

                if len(vcenter) > 0:
                    vcenter = vcenter[0]
                else:
                    vcenter = None
                    logger.warning('Atlas: could not find vcenter for host: %s' % url)

                results.append(Host(
                    name=name,
                    address=url,
                    site=site,
                    server_state=status,
                    vcenter=vcenter
                ))

        return results

from interfaces.host import Host
from interfaces.vcenter import Vcenter
from modules.helper.FileHelper import FileHelper

from typing import List

import re
import logging

logger = logging.getLogger('esxi')


class Atlas():
    def __init__(self, atlas_file: str) -> None:
        self.atlas_file = atlas_file
        self.re_site = re.compile(r'([A-Z]{2}\-[A-Z]{2}\-[0-9])[a-z]', re.IGNORECASE)

    def load_data(self):
        return FileHelper.get_json_dict(self.atlas_file)

    def get_vcenters(self) -> List[Vcenter]:
        """
        Get all vcenters. Raise SystemExit if somethihg goes wrong.

        :return: list of interfaces.Vcenter
        """

        logger.debug('getting vcenters from atlas...')

        results = []

        for target in self.load_data():
            if target['labels']['job'] == 'vcenter':
                results.append(Vcenter(
                    name=target['labels']['server_name'],
                    address=target['labels']['server_name'],
                )
                )
        return results

    def get_esxi_hosts(self) -> List[Host]:
        """
        Get all esxi-hosts. Returns a list of Host

        :return: list of Host
        """

        logger.debug('getting esxi-hosts from atlas...')

        results = []
        vcenters = self.get_vcenters()

        for target in self.load_data():
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

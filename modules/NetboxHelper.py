from datetime import datetime, timedelta
import logging
from os import getenv

import pynetbox
import requests

import modules.Configuration as config

logger = logging.getLogger('esxi-exporter')


class NetboxHelper:

    def __init__(self):
        session = requests.Session()
        session.verify = False
        self.netbox = pynetbox.api(getenv('NETBOX_URL'))
        self.netbox.http_session = session

        self.hosts = set()
        self.last_update = datetime.now()
        self.region = getenv('VCENTER_URL').split(".")[2]

    def is_host_active(self, host: str) -> bool:
        if self.last_update + timedelta(minutes=config.cachetime) < datetime.now() or len(self.hosts) == 0:
            self.update_hosts(self.region)
            self.last_update = datetime.now()
        return host in self.hosts

    def update_hosts(self, region: str):
        logger.info("getting active hosts from netbox...")
        try:
            _hosts = []
            for device in self.netbox.dcim.devices.filter(platform='vmware-esxi', region=region, status='active'):
                _hosts.append(device.name)
            self.hosts = _hosts.copy()
            logger.info("%i active hosts in region" % len(self.hosts))
        except Exception as ex:
            logger.error("update hosts failed: %s" % str(ex))

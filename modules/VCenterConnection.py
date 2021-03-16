import logging
import socket

import pyVim.connect
from pyVmomi import vim

from modules.Exceptions import VCenterDNSException, VCenterLoginException

# Init Logging
logger = logging.getLogger('esxi-exporter')


# inspired by pyCCloud VCenterHelper
class VcenterConnection:
    def __init__(self, host: str, user: str, password: str, verify_ssl: bool = False):
        self.api = None
        self.host = host
        self.user = user
        self.password = password
        self.verify_ssl = verify_ssl
        if verify_ssl:
            self._connect_class = pyVim.connect.SmartConnect
        else:
            logger.warning('vCenter connection with ssl disabled')
            self._connect_class = pyVim.connect.SmartConnectNoSSL
        self.login()

    def login(self):
        logger.info('vCenter logging in...')
        try:
            self.api = self._connect_class(
                protocol='https', host=self.host, user=self.user, pwd=self.password)
            logger.info('successfuly logged into vCenter')
        except socket.gaierror:
            message = 'Name or service not known: %s' % self.host
            logger.error(message)
            raise VCenterDNSException(message)
        except vim.fault.InvalidLogin:
            message = 'Wrong credentials %s' % self.host
            logger.error(message)
            raise VCenterLoginException

    def get_hosts(self):
        host_view = self.api.content.viewManager.CreateContainerView(self.api.content.rootFolder, [vim.HostSystem],
                                                                     True)
        host_list = [host for host in host_view.view]
        host_view.Destroy()
        return host_list

    def is_alive(self):
        try:
            self.api.CurrentTime()
            return True
        except (vim.fault.NotAuthenticated, http.client.RemoteDisconnected):
            return False

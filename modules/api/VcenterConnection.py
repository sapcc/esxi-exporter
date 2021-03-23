from interfaces.host import Host
from interfaces.vcenter import Vcenter

from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect

import logging
import socket

# Init Logging
from modules.Exceptions import VcenterError

logger = logging.getLogger('esxi-exporter')


class VcenterConnection:
    def __init__(self, host: str, user: str, password: str, verify_ssl: bool = False):
        """
        Provides functionality to fetch overall state of esxi host-systems.

        :param host: The url to the vcenter without https. You must use url not
        ip-address.
        :param user: The username used to login
        :param password: The password used to login
        :param verify_ssl: Should ssl certificates be verified? Default = False.
        """

        self.api = None
        self.host = host
        self.user = user
        self.password = password
        self.verify_ssl = verify_ssl
        if verify_ssl:
            self._connect_class = SmartConnect
        else:
            logger.warning('vCenter connection with ssl disabled: %s' % host)
            self._connect_class = SmartConnectNoSSL

    def login(self) -> None:
        logger.debug('vCenter logging in: %s' % self.host)
        try:
            self.api = self._connect_class(protocol='https', host=self.host,
                                           user=self.user, pwd=self.password)
            logger.debug('successfully logged into vCenter: %s' % self.host)

        except socket.gaierror as ex:
            message = 'Vcenter: DNS error, could not resolve name: %s' % self.host
            logger.error(message)
            raise VcenterError(message) from ex
        except vim.fault.InvalidLogin as ex:
            message = 'Vcenter: wrong credentials: %s' % self.host
            logger.error(message)
            raise VcenterError(message) from ex

    def is_alive(self) -> bool:
        if self.api is None:
            return False
        try:
            self.api.CurrentTime()
            return True
        except (vim.fault.NotAuthenticated, http.client.RemoteDisconnected):
            return False

    def disconnect(self) -> None:
        if self.api is not None:
            Disconnect(self.api)

    def _get_obj(self, root, vim_type):
        """
        Creates a ContainterView and returns it. Can be used to fetch all
        hosts or vms in one turn.

        :param root: The root where to start. eg vcenter.content.root
        :param vim_type: vimtype eg vim.HostSystem or vim.vm
        :return: ContainerView
        """

        container = self.api.content.viewManager.CreateContainerView(
            root, vim_type, True)
        view = container.view
        container.Destroy()
        return view

    @staticmethod
    def _create_filter_spec(pc, esxi_hosts, prop):
        """
        Build a filter spec (some kind of sql_query) for the property
        collector.
        See community samples
        https://github.com/vmware/pyvmomi-community-samples/blob
        /bc14f63065aa360ceca0cca477a8b271d582a090/samples/filter_vms.py

        :param pc: The property_collector
        :param esxi_hosts: a ContainerView of vim.HostSystem (Get with get_obj
        :param prop: a single string or list of strings. Properties to
        collect. Eg name, overallStatus...
        :return: the created filter spec
        """

        if not isinstance(prop, list):
            prop = [prop]

        objSpecs = []
        for host in esxi_hosts:
            objSpec = vmodl.query.PropertyCollector.ObjectSpec(obj=host)
            objSpecs.append(objSpec)
        filterSpec = vmodl.query.PropertyCollector.FilterSpec()
        filterSpec.objectSet = objSpecs
        propSet = vmodl.query.PropertyCollector.PropertySpec(all=False)
        propSet.type = vim.HostSystem
        propSet.pathSet = prop
        filterSpec.propSet = [propSet]
        return filterSpec

    def get_esxi_overall_stats(self):
        """
        Get the overall status of all esxi-hosts from vcenter.
        Status can be green, yellow or red.

        :return: a list of interfaces.Host
        """

        try:
            self.login()
            esxi = self._get_obj(self.api.content.rootFolder, [vim.HostSystem])
            pc = self.api.content.propertyCollector
            filter_spec = self._create_filter_spec(
                pc, esxi, ['overallStatus', 'name'])
            options = vmodl.query.PropertyCollector.RetrieveOptions()
            result = pc.RetrievePropertiesEx([filter_spec], options)

            res = []
            vcenter = Vcenter(name=self.host, address=self.host)

            state_map = {
                'green': 2, 'yellow': 1, 'red': 0,
            }

            for item in result.objects:
                name = [v.val for v in item.propSet if v.name == 'name'][0]
                status = [v.val for v in item.propSet if v.name ==
                          'overallStatus'][0]
                host = Host(name=name, address=name, overall_status=state_map[status],
                            vcenter=vcenter)
                res.append(host)

            return res

        except Exception as ex:
            raise VcenterError('Vcenter: unknown error') from ex
        finally:
            self.disconnect()

        return None

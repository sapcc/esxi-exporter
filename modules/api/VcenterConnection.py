from interfaces.host import Host
from interfaces.vcenter import Vcenter

from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect

import logging
import socket

# Init Logging
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
            logger.warning('vCenter connection with ssl disabled')
            self._connect_class = SmartConnectNoSSL

    def login(self) -> None:

        logger.debug('vCenter logging in...')
        try:
            self.api = self._connect_class(protocol='https', host=self.host,
                                           user=self.user, pwd=self.password)
            logger.debug('successfuly logged into vCenter')
        # todo: fix that below
        except socket.gaierror:
            message = 'Name or service not known: %s' % self.host
            logger.error(message)
        except vim.fault.InvalidLogin:
            message = 'Wrong credentials %s' % self.host
            logger.error(message)

    def is_alive(self) -> bool:
        if self.api is None:
            return None

        try:
            self.api.CurrentTime()
            return True
        except (vim.fault.NotAuthenticated, http.client.RemoteDisconnected):
            return False

    def disconnect(self) -> None:
        Disconnect(self.api)

    def _get_obj(self, root, vim_type):
        """
        Creates a ContainterView and returns it. Can be used to fetch all
        hosts or vms in one turn.

        :param root: The root where to start. eg vcenter.content.root
        :param vim_type: vimtype eg vim.HostSystem or vim.vm
        :return: ContainerView
        """

        container = self.api.content.viewManager.CreateContainerView(root, vim_type, True)
        view = container.view
        container.Destroy()
        return view

    @staticmethod
    def _create_filter_spec(pc, esxi, prop):
        """
        Build a filter spec (some kind of sql_query) for the property
        collector.
        See community samples
        https://github.com/vmware/pyvmomi-community-samples/blob
        /bc14f63065aa360ceca0cca477a8b271d582a090/samples/filter_vms.py

        :param pc: The property_collector
        :param esxi: a ContainerView of vim.HostSystem (Get with get_obj
        :param prop: a single string or list of strings. Properties to
        collect. Eg name, overallStatus...
        :return: the created filter spec
        """

        if not isinstance(prop, list):
            prop = [prop]

        objSpecs = []
        for host in esxi:
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
            filter_spec = self._create_filter_spec(pc, esxi, ['overallStatus', 'name'])
            options = vmodl.query.PropertyCollector.RetrieveOptions()
            result = pc.RetrievePropertiesEx([filter_spec], options)

            res = []
            vcenter = Vcenter(name=self.host, address=self.host)

            state_map = {
                'green': 2, 'yellow': 1, 'red': 0,
            }

            for item in result.objects:
                name = [v.val for v in item.propSet if v.name == 'name'][0]
                status = [v.val for v in item.propSet if v.name == 'overallStatus'][0]
                host = Host(name=name, address=name, overall_status=state_map[status],
                            vcenter=vcenter)
                res.append(host)

            return res

        except Exception as ex:
            raise ex
        finally:
            self.disconnect()

        return None

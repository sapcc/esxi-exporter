from interfaces.host import Host
from interfaces.vcenter import Vcenter

from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect

from typing import List

import master_password
import logging
import socket

# Init Logging
logger = logging.getLogger('esxi-exporter')


class VcenterConnection:
    def __init__(self, host: str, user: str, password: str, mpw: str = None, verify_ssl: bool = False):
        """
        Provides functionality to fetch overall state of esxi host-systems.

        :param host: The url to the vcenter without https. You must use url not
        ip-address.
        :param user: The username used to login.
        :param password: The password used to login.
        :param mpw: Alternative to normal password. Uses master_password mechanism and has precedence.
        :param verify_ssl: Should ssl certificates be verified? Default = False.
        """

        self.api = None
        self.host = host
        self.user = user
        self.password = self.choose_password(password, mpw)
        self.verify_ssl = verify_ssl
        if verify_ssl:
            self._connect_class = SmartConnect
        else:
            logger.warning('vCenter connection with ssl disabled: %s' % host)
            self._connect_class = SmartConnectNoSSL

    def choose_password(self, password, mpw) -> str:
        """
        Returns vcenter password. Master_password has precedence.
        One param may be None.

        :param password: Normal vcenter password.
        :param mpw: if not None it has precedence
        :return: password
        """
        if mpw is not None:
            # vcenter does not support slash char '/'
            return master_password.MPW(self.user, mpw).password(self.host).replace('/', '')
        elif password is not None:
            return password
        else:
            raise ValueError('No vcenter password provided')

    def login(self) -> bool:
        logger.debug('vCenter logging in: %s' % self.host)
        try:
            self.api = self._connect_class(protocol='https', host=self.host,
                                           user=self.user, pwd=self.password)
            logger.debug('successfully logged into vCenter: %s' % self.host)
            return True

        except socket.gaierror:
            message = 'Vcenter: DNS error, could not resolve name: %s' % self.host
            logger.error(message)
            return False
        except vim.fault.InvalidLogin as ex:
            message = 'Vcenter: wrong credentials: %s' % self.host
            logger.error(message)
            return False

    def disconnect(self) -> None:
        """
        Disconnect from vCenter. Does not matter if there is a connection.
        """
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
    def _create_filter_spec(esxi_hosts, prop):
        """
        Build a filter spec (some kind of sql_query) for the property
        collector.
        See community samples
        https://github.com/vmware/pyvmomi-community-samples/blob
        /bc14f63065aa360ceca0cca477a8b271d582a090/samples/filter_vms.py

        :param esxi_hosts: a ContainerView of vim.HostSystem (Get with get_obj
        :param prop: a single string or list of strings. Properties to
        collect. Eg name, overallStatus...
        :return: the created filter spec
        """

        if not isinstance(prop, list):
            prop = [prop]

        objSpecs = list()
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

    def get_esxi_overall_stats(self) -> List[Host]:
        """
        Get the overall status of all esxi-hosts from vcenter.
        Status can be green, yellow or red.

        :return: a list of interfaces.Host
        """

        if self.login():
            # prepare property collector and get results
            esxi = self._get_obj(self.api.content.rootFolder, [vim.HostSystem])
            pc = self.api.content.propertyCollector
            filter_spec = self._create_filter_spec(
                esxi, ['overallStatus', 'name'])
            options = vmodl.query.PropertyCollector.RetrieveOptions()
            result = pc.RetrievePropertiesEx([filter_spec], options)

            res = list()
            vcenter = Vcenter(name=self.host, address=self.host)

            state_map = {
                'green': 2, 'yellow': 1, 'red': 0,
            }

            # parse property collector
            for item in result.objects:
                name = [v.val for v in item.propSet if v.name == 'name']
                status = [v.val for v in item.propSet if v.name == 'overallStatus']
                if len(name) > 0 or len(status) > 0:
                    name = name[0]
                    status = status[0]
                else:
                    continue

                host = Host(name=name, address=name, overall_status=state_map[status],
                            vcenter=vcenter, site=vcenter.site)
                res.append(host)

            self.disconnect()
            return res

        return list()

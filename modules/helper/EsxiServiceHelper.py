from interfaces.host import Host
from modules.api.Atlas import Atlas
from modules.api.SshHelper import SshHelper

from typing import List

import concurrent.futures
import logging

logger = logging.getLogger('esxi')


class EsxiServiceHelper:

    def __init__(self, atlas: Atlas, esxi_username: str, esxi_password: str, monitored_services, max_threads: int):
        """
        Helper providing functionality to query critical service stats of esxi-host
        """

        self.atlas = atlas
        self.esxi_username = esxi_username
        self.esxi_password = esxi_password
        self.max_threads = max_threads

        self._services = monitored_services
        command_list = ["/etc/init.d/%s status" %
                        service for service in self._services]
        self._command = ' & '.join(command_list)

        # Strange bug. Display name is different from registered service name
        self._services = [item.replace('nsx-opsagent', 'opsAgent')
                          for item in self._services]

    def _concurrent_fetch_host_services(host: Host, ssh_username: str, ssh_password: str,
                                        command: str, services: list, output: list):
        """
        Multithreaded worker for concurrent ThreadPoolExecutor.
        Used to get services via SSH-Connections to esxi-hosts.
        """

        response = SshHelper.execute_ssh_command(
            host.address,
            ssh_username,
            ssh_password,
            command
        )

        host.services = {}  # init / reset services
        if response is None:
            logger.error('Could not fetch any services for host: %s' % host.name)
            return

        # loop over all critical services and try to find them in the response
        response = response.splitlines()
        for service in services:
            for line in response:
                if service in line and 'is running' in line:
                    host.services[service] = True
                    # check next service
                    break
                else:
                    host.services[service] = False
                    
        output.append(host)

    def get_all_service_stats(self) -> List[Host]:
        """
        Get all critical service stats of all listed esxi-hosts.

        :return: List of Host
        """

        # get hosts
        hosts = self.atlas.get_esxi_hosts()

        # Use ThreadPoolExecuter and store results in output
        output = list()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            for host in hosts:
                executor.submit(
                    EsxiServiceHelper._concurrent_fetch_host_services,
                    host,
                    self.esxi_username,
                    self.esxi_password,
                    self._command,
                    self._services,
                    output
                )

        return output

from modules.configuration.Configuration import Configuration
from interfaces.host import Host
from modules.api.Atlas import Atlas
from modules.api.SshHelper import SshHelper

from threading import Thread
from queue import Queue

import logging


logger = logging.getLogger('esxi')


class EsxiServiceHelper:

    def __init__(self, config: Configuration) -> None:
        self.atlas = Atlas(config)
        self.config = config

        self._services = self.config.monitored_serivces
        command_list = ["/etc/init.d/%s status" %
                        service for service in self._services]
        self._command = ' & '.join(command_list)

        # Strange bug. Display name is different from registered service name
        self._services = [item.replace('nsx-opsagent', 'opsAgent')
                          for item in self._services]

    def _worker(q: Queue, ssh_username: str, ssh_password: str,
                command: str, services: list, output: list):
        while not q.empty():
            host: Host = q.get()

            answer = SshHelper.execute_command(
                host.address,
                ssh_username,
                ssh_password,
                command
            )

            host.services = {}
            if answer is None:
                host.services = {k: False for k in services}
                # Maybe add some info to host that something is wrong?
                output.append(host)
                continue

            answer = answer.splitlines()
            for service in services:
                for line in answer:
                    if service in line and 'is running' in line:
                        host.services[service] = True
                        # check next service
                        break
                    else:
                        host.services[service] = False
            output.append(host)

    def get_all_service_stats(self) -> list:
        # get hosts
        hosts = self.atlas.get_esxi_hosts()

        # get services
        q = Queue()
        [q.put(host) for host in hosts]

        threads = []
        output = []
        for i in range(self.config.ssh_max_threads):
            t = Thread(target=EsxiServiceHelper._worker, args=(
                q,
                self.config.esxi_user,
                self.config.esxi_password,
                self._command,
                self._services,
                output
            ))
            threads.append(t)
            t.start()

        [t.join() for t in threads]

        return output

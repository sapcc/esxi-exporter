from interfaces.vcenter import Vcenter
from interfaces.host import Host
from modules.api.Atlas import Atlas
from modules.api.SshHelper import SshHelper
from modules.Globals import Globals
from modules.TimedBlacklist import TimedBlacklist

from threading import Thread
from queue import Queue

import logging

logger = logging.getLogger('esxi')

class EsxiServiceHelper:

    def __init__(self) -> None:
        self.atlas = Atlas()
        self.globals = Globals()
        self.blacklist = TimedBlacklist()


        self._services = self.globals.collectors.critical_service_collector.services
        command_list = ["/etc/init.d/%s status" %
                        service for service in self._services]
        self._command = ' & '.join(command_list)

        # Strange bug. Display name is different from registered service name
        self._services = [item.replace('nsx-opsagent', 'opsAgent')
                          for item in self._services]

    def _worker(q: Queue, ssh_username: str, ssh_password: str, command: str, services: list, output: list):
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
        for i in range(self.globals.collectors.critical_service_collector.max_threads):
            t = Thread(target=EsxiServiceHelper._worker, args=(
                q,
                self.globals.esxi_user,
                self.globals.esxi_password,
                self._command,
                self._services,
                output
            ))
            threads.append(t)
            t.start()

        [t.join() for t in threads]

        return output

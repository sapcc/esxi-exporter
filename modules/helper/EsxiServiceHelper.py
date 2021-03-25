
from modules.helper.GeneralHelper import GeneralHelper
from interfaces.host import Host
from modules.api.SshHelper import SshHelper

from threading import Thread
from queue import Queue
from typing import List

import logging

logger = logging.getLogger('esxi')


class EsxiServiceHelper:

    def __init__(self, esxi_username: str, esxi_password: str, monitored_services, max_threads: int) -> None:
        """
        Helper providing functionality to query critical service stats of esxi-host
        """


        self.general_helper = GeneralHelper()
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

    def _worker(host_queue: Queue, ssh_username: str, ssh_password: str,
                command: str, services: list, output: list):
        """
        Multithreaded worker. Used for SSH-Connections to esxi-hosts
        """

        while not host_queue.empty():
            host: Host = host_queue.get()

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

            # loop over all critical services and try to find them in the answer
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

    def get_all_service_stats(self) -> List[Host]:
        """
        Get all critical service stats of all listed esxi-hosts.

        :return: List of Host
        """

        # get hosts
        hosts = self.general_helper.get_esxi_hosts()

        # get services
        host_queue = Queue()
        [host_queue.put(host) for host in hosts]


        # Explaination of applied multihreading approach:
        # Imagine 10 threads operating as workers
        # Each worker gets a shared queue with 'tasks' - in this case a list of hosts to process
        # All workers operate and take jobs(hosts) from the queue-stack until it is empty.
        # If empty - the workers will stop and the join releases.
        # All Python base types are considered thread-safe, so a queue should be safe too.
        # Since the threads are separated and communication is tricky - a reference to a
        # thread_safe output variable is passed, where the results will be stored in.

        threads = []
        output = []
        for i in range(self.max_threads):
            t = Thread(target=EsxiServiceHelper._worker, args=(
                host_queue,
                self.esxi_username,
                self.esxi_password,
                self._command,
                self._services,
                output
            ))
            threads.append(t)
            t.start()

        [t.join() for t in threads]

        return output

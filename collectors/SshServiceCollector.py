import logging
from collections import defaultdict
from os import getenv
from queue import Queue
from threading import Thread

import paramiko
from prometheus_client.core import GaugeMetricFamily

import modules.TimedBlacklist as blacklist
from BaseCollector import BaseCollector
from modules.Exceptions import SSHEsxiClientException

logger = logging.getLogger('esxi-exporter')


class SshServiceCollector(BaseCollector):

    def __init__(self):
        super().__init__()

        self._monitoredServices = ['hostd', 'nsx-opsagent', 'nsx-proxy', 'nsxa', 'ntpd', 'vpxa', 'vvold']
        logger.info("monitoring: " + ', '.join(self._monitoredServices))

        command_list = ["/etc/init.d/%s status" % service for service in self._monitoredServices]
        self._query_command: str = ' & '.join(command_list)
        logger.info('compiled ssh command: ' + self._query_command)

    @staticmethod
    def ssh_worker(hosts: Queue, esxi_username: str, esxi_password: str, command: str, monitored_services: list,
                   output: dict) -> None:
        """
        To be used with a thread. Uses a queue as list of hosts to be monitored

        :param q: The queue containing esxi hosts as string
        :param esxi_username: the ssh username to login into the esxi host
        :param esxi_password: the ssh password to login into the esxi host
        :param command: the precompiled command which will run on all esxi in order to collect service stats
        :param monitored_services: a list of services to monitor
        :param output: a dictionary where the collected data will be returned
        :return:
        """
        # get task
        while not hosts.empty():
            host = hosts.get()

            try:

                output[host] = {}
                for srv in monitored_services:
                    output[host][srv] = False

                # connect
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname=host, username=esxi_username, password=esxi_password)

                # fetch data
                stdin, stdout, stderr = client.exec_command(command, timeout=2)
                answer = stdout.read().decode("utf-8")
                client.close()

                # parse data
                for service in monitored_services:
                    if ('%s is running' % service) in answer:
                        output[host][service] = True

            # Catch non critical exceptions otherwise crash... (eg paramiko.ConfigParserError)
            except (
            paramiko.BadAuthenticationType, paramiko.AuthenticationException, paramiko.PasswordRequiredException) as ex:
                logger.warning("Could not ssh login to: %s. Reason: %s" % (host, str(ex)))
                blacklist.add_host(host)
            except (paramiko.BadHostKeyException, paramiko.ChannelException, paramiko.SSHException,
                    paramiko.ProxyCommandFailure) as ex:
                logger.warning("Couldn't ssh connect to esxi-host via ssh: %s. Reason: %s" % (host, str(ex)))
            except Exception as ex:
                logger.error(str(ex))
                raise SSHEsxiClientException(str(ex)) from ex

    def describe(self):
        yield GaugeMetricFamily('esxi_ssh_service_state', 'health status of esxi-host services collected via ssh')

    def collect(self):
        """
        Collects data about critical services from esxi-hosts via a ssh connection

        :return:
        """

        results = defaultdict()
        tasks = Queue()

        # basically a template for a gauge metric
        gauge_metric = GaugeMetricFamily('esxi_ssh_service_state', '1=running, 0=stopped',
                                         labels=['vcenter', 'hostsystem', 'service'])

        # get hosts
        hosts = self.get_active_hosts()
        for host in hosts:
            tasks.put(host.name)

        # Creates a thread pool
        threads = []
        for i in range(int(getenv('ssh_threads', 10))):
            t = Thread(target=SshServiceCollector.ssh_worker, args=(
                tasks, getenv('ESXI_USER', 'root'), getenv('ESXI_PASSWORD'), self._query_command,
                self._monitoredServices, results))
            t.start()
            threads.append(t)

        # wait for threads to finish
        [t.join() for t in threads]

        # build metric
        for host, services in results.items():
            for svc_name, svc_state in services.items():
                gauge_metric.add_metric(labels=[getenv('VCENTER_URL'), host, svc_name], value=svc_state)

        yield gauge_metric

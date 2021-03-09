import logging
from datetime import datetime, timedelta
from queue import Queue
from threading import Thread

import paramiko
from prometheus_client.core import GaugeMetricFamily

from BaseCollector import BaseCollector
from modules.Configuration import Configuration
from modules.Exceptions import SSHEsxiClientException, SshCollectorException
from modules.NetboxHelper import NetboxHelper
from modules.VCenterConnection import VCenterConnection
from modules.TimedBlacklist import TimedBlacklist

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class SshServiceCollector(BaseCollector):

    def __init__(self, config: Configuration):
        """
        :param config: The config which provides credentials etc.
        """
        self._config = config

        logger.info('connecting to vcenter: ' + config.vCenter)
        self._conn = VCenterConnection(config.vCenter, config.vCenter_username, config.vCenter_password)
        self.netbox = NetboxHelper(self._config)

        self._results = {}
        self._blacklist = TimedBlacklist(config.blacklisttime)
        self._tasks = Queue()
        self._monitoredServices = ['hostd', 'nsx-opsagent', 'nsx-proxy', 'nsxa', 'ntpd', 'vpxa', 'vvold']

        logger.info("monitoring: " + ', '.join(self._monitoredServices))

        # The command executed on the esxi gets concatenated in
        # order to minimize requests since there are not so many
        # services to watch
        # Furthermore a class-scoped variable should reduce runtime redundancy
        command_list = ["/etc/init.d/%s status" % service for service in self._monitoredServices]
        self._query_command: str = ' & '.join(command_list)
        logger.info('compiled ssh command: ' + self._query_command)

    @staticmethod
    def ssh_worker(q: Queue, esxi_username: str, esxi_password: str, command: str, monitored_services: list,
                   blacklist: TimedBlacklist, output: dict) -> None:
        """
        To be used with a thread. Uses a queue as list of hosts to be monitored

        :param q: The queue containing esxi hosts as string
        :param esxi_username: the ssh username to login into the esxi host
        :param esxi_password: the ssh password to login into the esxi host
        :param command: the precompiled command which will run on all esxi in order to collect service stats
        :param monitored_services: a list of services to monitor
        :param blacklist: a blacklists for hosts which failed to connect
        :param output: a dictionary where the collected data will be returned
        :return:
        """
        # get task
        while not q.empty():
            host = q.get()

            try:
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

            # Exceptions
            # -----------
            # AuthenticationException,
            # BadAuthenticationType,
            # BadHostKeyException,
            # ChannelException,
            # ConfigParseError,
            # CouldNotCanonicalize,
            # PasswordRequiredException,
            # ProxyCommandFailure,
            # SSHException,

            # Catch non critical exceptions otherwise crash... (eg ConfigParserError)            
            except (
            paramiko.BadAuthenticationType, paramiko.AuthenticationException, paramiko.PasswordRequiredException) as ex:
                logger.warning("Could not ssh login to: %s. Reason: %s" % (host,str(ex)))
                blacklist.add_host(host)
            except (paramiko.BadHostKeyException, paramiko.ChannelException, paramiko.SSHException,
                    paramiko.ProxyCommandFailure) as ex:
                logger.warning("Couldn't ssh connect to esxi-host via ssh: %s. Reason: %s" % (host, str(ex)))
            except Exception as ex:
                logger.error(str(ex))
                raise SSHEsxiClientException(str(ex)) from ex

    def collect(self):
        """
        Collects data about critical services from esxi-hosts via a ssh connection

        :return:
        """

        starttime = datetime.now()

        # basically a template for a gauge metric
        # todo: is this state label there correct? if not see also other collectors
        gauge_metric = GaugeMetricFamily('esxi_ssh_service_state', '1=running, 0=stopped',
                                         labels=['vcenter', 'host', 'service'])

        # check connection state
        if not self._conn.is_alive():
            self._conn = VCenterConnection(self._config.vCenter, self._config.vCenter_username,
                                           self._config.vCenter_password)

        # get hosts
        hosts = self._conn.get_hosts()

        # filter hosts (netbox > active)
        hosts = [host for host in hosts if
                 self.netbox.is_host_active(host.name.split('.')[0]) and self._blacklist.is_host_allowed(host.name)]
        logger.info('vCenter returned %i hosts' % len(hosts))

        # init results
        self._results = {}
        self._tasks = Queue()
        for host in hosts:
            node = host.name
            self._tasks.put(host.name)
            self._results[node] = {}
            for srv in self._monitoredServices:
                self._results[node][srv] = False

        # Creates a thread pool
        threads = []
        for i in range(self._config.ssh_threads):
            t = Thread(target=SshServiceCollector.ssh_worker, args=(
                self._tasks, self._config.esxi_username, self._config.esxi_password, self._query_command,
                self._monitoredServices, self._blacklist, self._results))
            t.start()
            threads.append(t)

        # wait for threads to finish
        [t.join() for t in threads]

        # build metric
        for host, services in self._results.items():
            for svc_name, svc_state in services.items():
                gauge_metric.add_metric(labels=[self._config.vCenter, host, svc_name], value=svc_state)

        deltatime = datetime.now() - starttime
        logger.info('operation took %i seconds' % deltatime.seconds)

        yield gauge_metric

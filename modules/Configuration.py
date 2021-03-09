import logging
from optparse import OptionParser
from os import getenv

from modules.Exceptions import ConfigException

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class Configuration:

    @staticmethod
    def parse_params():
        parser = OptionParser()
        parser.add_option("-o", "--port", help="The port where the prometheus server should run", action="store",
                          dest="port", type="int")
        parser.add_option("--vsc_user", help="The username for the vCenter", action="store", dest="vCenter_username",
                          type="string")
        parser.add_option("--vsc_password", help="The password for the vCenter user", action="store",
                          dest="vCenter_password", type="string")
        parser.add_option("--esxi_user", help="The username for the vCenter", action="store", dest="esxi_username",
                          type="string")
        parser.add_option("--esxi_password", help="The password for the vCenter user", action="store",
                          dest="esxi_password", type="string")
        parser.add_option("-t", "--target", help="The address of the vCenter without https://", action="store",
                          dest="vCenter", type="string")
        parser.add_option("-x", "--noPyVim", help="Disable pyVimServiceCollector", action="store_true",
                          dest="pyVimDisable")
        parser.add_option("-z", "--noSSH", help="Disable ssh Service Collector",
                          action="store_true", dest="sshDisable")
        parser.add_option("-q", "--sshThreads", help="Disable ssh Service Collector", action="store",
                          dest="ssh_threads", type="int")
        parser.add_option("-n", "--netbox_url", help="The netbox url",
                          action="store", dest="netbox", type="string")
        parser.add_option("-i", "--blacklisttime", help="If a ssh connection fails, the host gets blacklisted for x minutes",
                          action="store", dest="blacklisttime", type="int")
        parser.add_option("-j", "--cashtime", help="The netbox url",
                          action="store", dest="cashtime", type="int")

        (options, args) = parser.parse_args()
        return options

    def check_configuration(self):
        logger.info("checking configuration...")

        # Null checks
        if self.port is None:
            raise ConfigException('No port was set')
        if self.ssh_threads is None or not self.ssh_threads > 0:
            raise ConfigException('No port was set')
        if self.vCenter is None or self.vCenter == '':
            raise ConfigException('No vCenter URL was set')
        if self.vCenter_username is None or self.vCenter_username == '':
            raise ConfigException('No vCenter user was set')
        if self.vCenter_password is None or self.vCenter_password == '':
            raise ConfigException('No vCenter password was set')
        if self.esxi_username is None or self.esxi_username == '':
            raise ConfigException('No esxi-host user was set')
        if self.esxi_password is None or self.esxi_password == '':
            raise ConfigException('No esxi-host password was set')
        if self.netbox is None or self.netbox == '':
            raise ConfigException("No netbox url was set")
        if self.cashtime is None:
            raise ConfigException('No cashtime was set')
        if self.blacklisttime is None:
            raise ConfigException('No blacklisttime was set')

        # Type Checks
        if not isinstance(self.port, int):
            raise ConfigException('Port is not instance of int')
        if not isinstance(self.pyVimDisable, bool):
            raise ConfigException('pyVimDisable is not instance of bool')
        if not isinstance(self.sshDisable, bool):
            raise ConfigException('sshDisable is not instance of bool')
        if not isinstance(self.ssh_threads, int):
            raise ConfigException('ssh_threads is not instance of bool')
        if not isinstance(self.blacklisttime, int):
            raise ConfigException('blacklisttime is not instance of int')
        if not isinstance(self.cashtime, int):
            raise ConfigException('cashtime is not instance of int')

        # logic checks
        if self.pyVimDisable == True & self.sshDisable == True:
            raise ConfigException(
                'You have disabled all collectors. At least one must be enabled.')

    def __init__(self):

        logger.info("loading configuration...")

        # get config from environment
        self.vCenter_username = getenv('vcenter_user')
        self.vCenter_password = getenv('vcenter_password')
        self.vCenter = getenv('vcenter_url')

        self.esxi_username = getenv('esxi_user', 'root')
        self.esxi_password = getenv('esxi_password')

        self.ssh_threads: int = int(getenv('ssh_threads', 10))
        self.pyVimDisable: bool = bool(getenv('disable_pyvim', False))
        self.sshDisable: bool = bool(getenv('disable_ssh', False))

        # todo: specify better default port
        self.port: int = int(getenv('exporter_port', 1234))
        self.netbox: str = getenv('netbox_url')
        self.cashtime: int = int(getenv('cashtime', 60))
        self.blacklisttime: int = int(getenv('blacklisttime', 20))

        # get config from cmd_args
        options = self.parse_params()

        # vCenter
        if options.vCenter_username is not None:
            self.vCenter_username = options.vCenter_username
        if options.vCenter_password is not None:
            self.vCenter_password = options.vCenter_password
        if options.vCenter is not None:
            self.vCenter = options.vCenter

        # esxi hosts
        if options.esxi_username is not None:
            self.esxi_username = options.esxi_username
        if options.esxi_password is not None:
            self.esxi_password = options.esxi_password

        if options.pyVimDisable is not None:
            self.pyVimDisable = options.pyVimDisable
        if options.sshDisable is not None:
            self.sshDisable = options.sshDisable

        # general
        if options.port is not None:
            self.port = int(options.port)
        if options.ssh_threads is not None:
            self.ssh_threads = int(options.ssh_threads)
        if options.netbox is not None:
            self.netbox = options.netbox
        if options.blacklisttime is not None:
            self.blacklisttime = options.blacklisttime
        if options.cashtime is not None:
            self.cashtime = options.cashtime

        self.check_configuration()

import logging
from os import getenv

from modules.Exceptions import ConfigException

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


logger.info("loading configuration...")

# get config from environment
vCenter_username = getenv('vcenter_user')
vCenter_password = getenv('vcenter_password')
vCenter = getenv('vcenter_url')

esxi_username = getenv('esxi_user', 'root')
esxi_password = getenv('esxi_password')

ssh_threads: int = int(getenv('ssh_threads', 10))
pyVimDisable: bool = bool(getenv('disable_pyvim', False))
sshDisable: bool = bool(getenv('disable_ssh', False))

# todo: specify better default port
port: int = int(getenv('exporter_port', 1234))
netbox: str = getenv('netbox_url')
cashtime: int = int(getenv('cashtime', 60))
blacklisttime: int = int(getenv('blacklisttime', 20))

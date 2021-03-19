from modules.api.VcenterConnection import VcenterConnection
from modules.Globals import Globals

config = Globals()
vcenter = VcenterConnection(config.vcenter_url, config.vcenter_user, config.vcenter_password)
hosts = vcenter.get_esxi_overall_stats()
print(".")
from modules.configuration.EnvironmentConfig import EnvironmentConfig
from modules.configuration.YamlConfig import YamlConfig
from modules.helper.VCenterHelper import VCenterHelper
from modules.api.Atlas import Atlas
from modules.helper.EsxiServiceHelper import EsxiServiceHelper


class UnifiedInterface:

    def __init__(self, yaml_config: YamlConfig, env_config: EnvironmentConfig) -> None:

        self.yaml_config = yaml_config
        self.env_config = env_config

        self.atlas = Atlas(env_config.atlas_file)
        self.esxi_helper = EsxiServiceHelper(self, env_config.esxi_user, env_config.esxi_password)
        self.vcenter_helper = VCenterHelper(self)


    def get_vcenters(self) -> list:
        return self.atlas.get_vcenters()

    def get_host_service_stats(self) -> list:
        return self.esxi_helper.get_all_service_stats()

    def get_host_overall_stats(self) -> list:
        return self.vcenter_helper.get_esxi_overall_stats()

    def get_hosts(self):
        return self.atlas.get_esxi_hosts()

    def get_vcenters(self):
        return self.atlas.get_vcenters()
from modules.configuration.ConfigMap import ConfigMap
from modules.Singleton import Singleton
import yaml


class YamlConfig(ConfigMap, metaclass=Singleton):

    def __init__(self) -> None:
        super().__init__()

        with open('config.yaml', 'rt', encoding='utf8') as f:
            data = yaml.safe_load(f)
        self.parse_dict(data)

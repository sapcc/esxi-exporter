from modules.configuration.ConfigMap import ConfigMap
from modules.Singleton import Singleton
import yaml
import logging

logger = logging.getLogger('esxi')


class YamlConfig(ConfigMap, metaclass=Singleton):

    def __init__(self) -> None:
        super().__init__()

        try:
            with open('config.yaml', 'rt', encoding='utf8') as f:
                data = yaml.safe_load(f)
            # Convert dict to attributes
            self.parse_dict(data)
        except yaml.YAMLError as ex:
            logger.error('Yaml: config file is not valid')
        except IOError:
            logger.error("Yaml: could not open file: config.yaml")

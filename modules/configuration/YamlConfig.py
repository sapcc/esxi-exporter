from modules.Exceptions import ConfigException
from os import EX_UNAVAILABLE
import yaml
import logging

logger = logging.getLogger('esxi')


class YamlConfig():

    def __init__(self):
        try:
            with open('config.yaml', 'rt', encoding='utf8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as ex:
            logger.error('Yaml: config file is not valid')
            raise SystemExit('Yaml: config file is not valid') from ex
        except IOError as ex:
            logger.error("Yaml: could not open file: config.yaml")
            raise SystemExit('Yaml: could not open file: config.yaml') from ex

        self.port = int(data['port'])

        self.enable_critical_serivce_collector = data['collectors']['critical_service_collector']['enabled']
        self.ssh_max_threads = data['collectors']['critical_service_collector']['max_threads']
        self.monitored_serivces =data['collectors']['critical_service_collector']['services']
        self.enable_overall_status_collector = data['collectors']['overall_state_collector']['enabled']

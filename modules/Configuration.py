import yaml
import logging

logger = logging.getLogger('esxi-exporter')

try:

    with open('config.yaml', 'r', encoding='utf8') as f:
        data = yaml.safe_load(f)

    port: int = int(data['port'])
    cashtime: int = int(data['cashtime'])
    blacklisttime: str = int(data['blacklisttime'])
    enable_pyvim: bool = 'pyvim' in data['collectors']
    enable_ssh: bool = 'ssh' in data['collectors']
    enable_overall_state: bool = 'overallstate' in data['collectors']
    del data

except KeyError as ex:
    logger.critical("Missing configuration entry: %s" % str(ex))
    exit(0)

except IOError as ex:
    logging.critical("Could not open config.yaml: %s" % str(ex))
    exit(0)

except TypeError as ex:
    logging.critical("Could not convert type: %s" % str(ex))
    exit(0)

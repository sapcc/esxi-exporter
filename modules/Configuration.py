import yaml
import logging

logger = logging.getLogger('esxi-exporter')

try:

    with open('config.yaml', 'r', encoding='utf8') as f:
        data = yaml.safe_load(f)

    port: int = int(data['port'])
    cachetime: int = int(data['cachetime'])
    blacklisttime: str = int(data['blacklisttime'])
    enable_pyvim: bool = 'pyvim' in data['collectors']
    enable_ssh: bool = 'ssh' in data['collectors']
    enable_overall_state: bool = 'overall_state' in data['collectors']
    ssh_services: list = data['ssh_collector']['services']
    ssh_threads: int = int(data['ssh_collector']['thread_count'])
    overallstate_threads: int = int(
        data['overall_state_collector']['thread_count'])
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

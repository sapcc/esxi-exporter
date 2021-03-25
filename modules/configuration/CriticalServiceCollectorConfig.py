from modules.helper.FileHelper import FileHelper

import os
import logging

logger = logging.getLogger('esxi')


class CriticalServiceCollectorConfig:

    def __init__(self):

        try:
            self.esxi_username = os.environ['ESXI_USER']
            self.esxi_password = os.environ['ESXI_PASSWORD']
        except KeyError as ex:
            logger.critical('Missing environment variable: %s' % str(ex))
            raise SystemExit() from ex

        yaml_dict = FileHelper.get_yaml_dict('config.yaml')
        self.max_threads = yaml_dict.setdefault('collectors', {}).setdefault('critical_service_collector',
                                                                             {}).setdefault('max_threads', 10)
        self.critical_services = yaml_dict.setdefault('collectors', {}).setdefault('critical_service_collector',
                                                                             {}).setdefault('services', [])

        if not len(self.critical_services) > 0:
            logger.critical('No critical services specified')
            raise ValueError('No critical servicbes specified')
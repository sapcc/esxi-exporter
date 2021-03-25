from modules.helper.FileHelper import FileHelper

import os
import logging

logger = logging.getLogger('esxi')


class CriticalServiceCollectorConfig:

    def __init__(self):
        self.esxi_username = os.environ['ESXI_USER']
        self.esxi_password = os.environ['ESXI_PASSWORD']

        yaml_dict = FileHelper.get_yaml_dict('config.yaml')
        self.max_threads = yaml_dict.get('collectors', {}).get('critical_service_collector',
                                                               {}).get('max_threads', 10)
        self.critical_services = yaml_dict.get('collectors', {}).get('critical_service_collector',
                                                                     {}).get('services', [])

        if not len(self.critical_services) > 0:
            logger.critical('No critical services specified')
            raise ValueError('No critical services specified')

import os
import logging

logger = logging.getLogger('esxi')


class OverallStateCollectorConfig:

    def __init__(self):
        try:
            self.vcenter_username = os.environ['VCENTER_USER']
            self.vcenter_password = os.environ['VCENTER_PASSWORD']
        except KeyError as ex:
            logger.critical('Missing environment variable: %s' % str(ex))
            raise SystemExit() from ex
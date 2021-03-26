import os
import logging

logger = logging.getLogger('esxi')


class OverallStateCollectorConfig:

    def __init__(self):
        self.vcenter_username = os.environ['VCENTER_USER']
        self.vcenter_password = os.getenv('VCENTER_PASSWORD', None)
        self.vcenter_master_password = os.getenv('VCENTER_MPW', None)

        if self.vcenter_password is None and self.vcenter_master_password is None:
            raise ValueError('No vcenter password was provided')
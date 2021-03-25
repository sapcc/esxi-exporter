import os
import logging

logger = logging.getLogger('esxi')


class OverallStateCollectorConfig:

    def __init__(self):
        self.vcenter_username = os.environ['VCENTER_USER']
        self.vcenter_password = os.environ['VCENTER_PASSWORD']

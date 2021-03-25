import os
import logging

logger = logging.getLogger('esxi')


class GeneralHelperConfig:
    def __init__(self):
        self.atlas_file = os.environ['ATLAS_FILE']

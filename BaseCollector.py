from modules.api.Atlas import Atlas
from modules.helper.FileHelper import FileHelper

from abc import ABC, abstractmethod

import logging
import os

logger = logging.getLogger('esxi')


class BaseCollector(ABC):

    def __init__(self):
        atlas_file = os.environ['ATLAS_FILE']
        self.atlas = Atlas(atlas_file)

        yaml_dict = FileHelper.get_yaml_dict(os.environ['CONFIG_FILE'])
        self.verify_ssl = yaml_dict.get('verify_ssl', True)

    @abstractmethod
    def collect(self):
        pass

    @abstractmethod
    def describe(self):
        pass

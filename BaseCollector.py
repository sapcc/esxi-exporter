from modules.configuration.Configuration import Configuration
from modules.UnifiedInterface import UnifiedInterface

from abc import ABC, abstractmethod

import logging

logger = logging.getLogger('esxi')


class BaseCollector(ABC):

    def __init__(self, config: Configuration):
        self.config = config
        self.unified_interface = UnifiedInterface(config)

    @abstractmethod
    def collect(self):
        pass

    @abstractmethod
    def describe(self):
        pass

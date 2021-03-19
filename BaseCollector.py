from abc import ABC, abstractmethod
from modules.UnifiedInterface import UnifiedInterface

import logging


logger = logging.getLogger('esxi-exporter')


class BaseCollector(ABC, UnifiedInterface):

    @abstractmethod
    def collect(self):
        pass

    @abstractmethod
    def describe(self):
        pass

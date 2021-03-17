from abc import ABC, abstractmethod
from os import getenv
from modules.NetboxHelper import NetboxHelper
from modules.VcenterConnection import VcenterConnection
from modules.UnifiedInterface import UnifiedInterface

import logging
import modules.TimedBlacklist as blacklist


logger = logging.getLogger('esxi-exporter')


class BaseCollector(ABC, UnifiedInterface):

    @abstractmethod
    def collect(self):
        pass

    @abstractmethod
    def describe(self):
        pass

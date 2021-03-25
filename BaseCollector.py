from abc import ABC, abstractmethod

import logging

logger = logging.getLogger('esxi')


class BaseCollector(ABC):

    @abstractmethod
    def collect(self):
        pass

    @abstractmethod
    def describe(self):
        pass

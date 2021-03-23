from modules.Exceptions import ExporterException
from modules.Singleton import Singleton
from modules.configuration.ArgumentsConfig import ArgumentsConfig
from modules.configuration.EnvironmentConfig import EnvironmentConfig
from modules.configuration.YamlConfig import YamlConfig

import logging

logger = logging.getLogger('esxi')


class Globals(metaclass=Singleton):

    def __init__(self) -> None:
        config_providers = [
            YamlConfig(),
            EnvironmentConfig(),
            ArgumentsConfig()
            ]

        for provider in config_providers:
            for k, v in provider.__dict__.items():
                self.__dict__[k] = v

    def __getattr__(self, item):
        logger.error("setting is not configured: %s" % item)
        raise ExporterException("Setting is not configured: %s" % item)

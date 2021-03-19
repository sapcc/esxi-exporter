from modules.configuration.EnvironmentConfig import EnvironmentConfig
from modules.configuration.YamlConfig import YamlConfig
from modules.configuration.ArgumentsConfig import ArguementsConfig
from modules.Singleton import Singleton


class Globals(metaclass=Singleton):

    def __init__(self) -> None:
        config_providers = [
            YamlConfig(),
            EnvironmentConfig(),
            ArguementsConfig()
        ]

        for provider in config_providers:
            for k,v in provider.__dict__.items():
                self.__dict__[k] = v

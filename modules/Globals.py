from modules.EnvironmentConfig import EnvironmentConfig
from modules.YamlConfig import YamlConfig
from modules.ArgumentsConfig import ArguementsConfig
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

    # def __getattr__(self, name: str) :
    #     for obj in self.config_providers:
    #         if name in obj.__dict__.keys():
    #             self.__dict__[name] = obj.__dict__[name]
    #             return self.__dict__[name]
    #         else:
    #             continue
    #     return None

    # def __setattr__(self, name: str, value) -> None:
    #     self.__dict__[name] = value


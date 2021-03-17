from modules.Singleton import Singleton
from os import environ


class EnvironmentConfig(metaclass=Singleton):

    def __init__(self) -> None:

        for key in [
            'ESXI_PASSWORD',
            'ESXI_USER',
            'VCENTER_USER',
            'VCENTER_PASSWORD'
        ]:
            self.__dict__[key] = environ[key]

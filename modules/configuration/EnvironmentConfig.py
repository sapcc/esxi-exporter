from modules.Singleton import Singleton
from os import environ


class EnvironmentConfig(metaclass=Singleton):
    """
    Provides configuration from environment variables.
    """


    def __init__(self) -> None:

        for key in [
            'ESXI_PASSWORD',
            'ESXI_USER',
            'VCENTER_USER',
            'VCENTER_PASSWORD',
            'ATLAS_FILE',
        ]:
            # add data as attributes to this class
            self.__dict__[key.lower()] = environ[key]

from modules.configuration.ArgumentsConfig import ArgumentsConfig
from modules.configuration.EnvironmentConfig import EnvironmentConfig
from modules.configuration.YamlConfig import YamlConfig


class Configuration(YamlConfig, ArgumentsConfig, EnvironmentConfig):
    """
    Configuration wrapper class
    """

    def __init__(self):
        # super(Configuration, self).init() did not work
        # therefore explicit init
        YamlConfig.__init__(self)
        ArgumentsConfig.__init__(self)
        EnvironmentConfig.__init__(self)

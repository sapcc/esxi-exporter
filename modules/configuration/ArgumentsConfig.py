from optparse import OptionParser
from modules.Singleton import Singleton


class ArgumentsConfig(metaclass=Singleton):

    def __init__(self) -> None:
        option_parser = OptionParser()
        option_parser.add_option('-d', '--debug', action='store_true', dest='debug', help='Enable debug output')
        option_parser.add_option('-v', '--info', action='store_true', dest='info', help='Enable info output')
        (options, args) = option_parser.parse_args()

        # add attributes dynamically from options to self
        # __dict__ represents all attributes of a class and can be modified
        self.__dict__ = options.__dict__

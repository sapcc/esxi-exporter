from optparse import OptionParser

import logging

logger = logging.getLogger('esxi')

class ArgumentsConfig():

    def __init__(self):
        option_parser = OptionParser()
        option_parser.add_option('-v', action='count', dest='debug', help='-v info; -vv debug output', default=0)

        (options, args) = option_parser.parse_args()

        if options.debug == 2:
            self.logging_mode = logging.DEBUG
        elif options.debug == 1:
            self.logging_mode = logging.INFO
        else:
            self.logging_mode = logging.WARNING

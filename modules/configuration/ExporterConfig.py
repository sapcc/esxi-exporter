from modules.helper.FileHelper import FileHelper
from argparse import ArgumentParser

import logging

logger = logging.getLogger('esxi')


class ExporterConfig:
    def __init__(self):
        arg_parser = ArgumentParser()
        arg_parser.add_argument('-v', action='count', dest='debug', default=0, help='-v info; -vv debug output')
        options = arg_parser.parse_args()

        if options.debug == 0:
            self.logging_mode = logging.WARNING
        elif options.debug == 1:
            self.logging_mode = logging.INFO
        elif options.debug == 2:
            self.logging_mode = logging.DEBUG
        else:
            raise ValueError('Console output flag passed by argumentparser is out of range[0;2]')

        yaml_dict = FileHelper.get_yaml_dict('config.yaml')
        self.port = yaml_dict.setdefault('port', 9666)
        self.enable_cricital_service_collector: bool = yaml_dict.setdefault('collectors', {}).setdefault(
            'critical_service_collector', {}).setdefault('enabled', False)

        self.enable_overall_state_collector: bool = yaml_dict.setdefault('collectors', {}).setdefault(
            'overall_state_collector', {}).setdefault('enabled', False)

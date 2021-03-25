import os
import logging

logger = logging.getLogger('esxi')


class GeneralHelperConfig:
    def __init__(self):
        try:
            self.atlas_file = os.environ['ATLAS_FILE']
        except KeyError as ex:
            logger.critical('Missing environment variable: %s' % str(ex))
            raise SystemExit() from ex

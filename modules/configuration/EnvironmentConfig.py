from os import environ

import logging

logger = logging.getLogger('esxi')

class EnvironmentConfig:
    """
    Provides configuration from environment variables.
    """

    def __init__(self):
        try:
            self.esxi_password = environ['ESXI_PASSWORD']
            self.esxi_user = environ['ESXI_USER']
            self.vcenter_user = environ['VCENTER_USER']
            self.vcenter_password = environ['VCENTER_PASSWORD']
            self.atlas_file = environ['ATLAS_FILE']
        except KeyError as ex:
            logger.error('EnvConfig: missing variable: %s' % str(ex))
            raise SystemExit('Missing environment variable') from ex
        except TypeError as ex:
            logger.error('EnvConfig: wrong type of variable: %s' % str(ex))
            raise SystemExit('Wrong type in environment variables')
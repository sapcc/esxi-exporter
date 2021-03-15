import datetime
import logging
from os import getenv

logger = logging.getLogger('esxi-exporter')

duration_minutes = int(getenv('BLACKLISTTIME', 20))
hosts = dict()


def add_host(hostname: str) -> None:
    logging.info('host got blacklisted: %s' % hostname)
    hosts[hostname] = datetime.datetime.now()


def remove_host(hostname: str) -> None:
    try:
        hosts.pop(hostname)
    except KeyError:
        # just delete, if key does not exists this is also okay.
        pass


def is_host_allowed(hostname: str) -> bool:
    try:
        # check if time is already over
        if hosts[hostname] + datetime.timedelta(minutes=duration_minutes) < datetime.datetime.now():
            remove_host(hostname)
            return True
        else:
            return False
    except KeyError:
        return True

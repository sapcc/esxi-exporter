import datetime

import modules.Configuration as config

duration_minutes = config.blacklisttime
hosts = dict()

def add_host(hostname: str) -> None:
    hosts[hostname] = datetime.datetime.now()

def remove_host( hostname: str) -> None:
    try:
        hosts.pop(hostname)
    except KeyError:
        # just delete, if key does not exists this is also okay.
        pass

def is_host_allowed( hostname: str) -> bool:
    try:
        # check if time is already over
        return hosts[hostname] + datetime.timedelta(
            minutes=duration_minutes) < datetime.datetime.now()
    except KeyError:
        return True

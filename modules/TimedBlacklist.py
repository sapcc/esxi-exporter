import datetime


class TimedBlacklist:

    def __init__(self, minutes: int) -> None:
        self.duration_minutes = minutes
        self._hosts = dict()

    def add_host(self, hostname: str) -> None:
        self._hosts[hostname] = datetime.datetime.now()

    def remove_host(self, hostname: str) -> None:
        try:
            self._hosts.pop(hostname)
        except Exception:
            pass

    def is_host_allowed(self, hostname: str) -> bool:
        try:
            return self._hosts[hostname] + datetime.timedelta(
                minutes=self.duration_minutes) < datetime.datetime.now()
        except KeyError:
            return True

class Blacklist:
    def __init__(self) -> None:
        self._hosts = set()

    def add_host(self, hostname: str):
        try:
            self._hosts.add(hostname)
        except Exception:
            pass

    def is_host_allowed(self, hostname: str) -> bool:
        return hostname not in self._hosts

    def remove_host(self, hostname: str):
        try:
            self._hosts.remove(hostname)
        except Exception:
            pass

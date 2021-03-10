class VCenterException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class VCenterLoginException(VCenterException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class VCenterDNSException(VCenterException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class SshCollectorException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class SSHEsxiClientException(SshCollectorException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ConfigException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

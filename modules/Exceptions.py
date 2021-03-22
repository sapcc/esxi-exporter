class ExporterException(Exception):
    pass


class AtlasError(ExporterException):
    pass


class VcenterError(ExporterException):
    pass


def ConfigException(ExporterException):
    pass

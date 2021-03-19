class Vcenter:

    def __init__(self, name: str, address: str, site=None) -> None:
        self.name = name
        self.address = address
        self.site = site

    @property
    def region(self):
        return self.name.split('.')[2]
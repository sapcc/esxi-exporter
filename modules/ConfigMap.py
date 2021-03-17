class ConfigMap:
    def parse_dict(self, data: dict) -> None:
        for k,v in data.items():
            if isinstance(v,dict):
                self.__dict__[k] = ConfigMap()
                self.__dict__[k].parse_dict(v)
            else:
                self.__dict__[k] = v
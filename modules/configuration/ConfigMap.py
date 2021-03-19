class ConfigMap:
    """
    Recursivly maps a dictionary to class attributes (self.__dict__) using itself as target
    """

    def parse_dict(self, data: dict) -> None:
        """
        Recursivly maps a dictionary to class attributes (self.__dict__) using itself as target

        :param data: The dictionary to convert to attributes
        :return:
        """
        for k,v in data.items():
            if isinstance(v,dict):
                self.__dict__[k] = ConfigMap()
                self.__dict__[k].parse_dict(v)
            else:
                self.__dict__[k] = v
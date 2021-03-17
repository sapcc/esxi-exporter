from modules.Singleton import Singleton


class UnifiedInterface(metaclass=Singleton):

    def get_hosts(self):
        pass

    def get_hosts_by_vcenter(self, name:str):
        pass





    

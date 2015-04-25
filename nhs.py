from icoolnamelistcontainer import *


class Nhs(ICoolNameListContainer):
    allowed_enclosed_commands = []

    command_params = {}

    def __init__(self, **kwargs):
        ICoolObject.check_command_params_init(self, **kwargs)
        Container.__init__(self)

    def __call__(self, **kwargs):
        #Need to figure out how to call container
        pass

    def __setattr__(self, name, value):
        self.__icool_setattr__(name, value)
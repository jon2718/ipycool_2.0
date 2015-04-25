from icoolnamelistcontainer import *
from beamtype import *


class Bmt(ICoolNameListContainer):

    allowed_enclosed_commands = ['BeamType']

    command_params = {
        'nbeamtyp': {
            'desc': '# of beam types, e.g., particles of different masses.',
            'doc': '',
            'type': 'Integer',
            'req': True,
            'default': 1},
        'bmalt': {
            'desc': 'if true => flip sign of alternate particles when BGEN = true.',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': False}}

    def __init__(self, **kwargs):
        ICoolObject.check_command_params_init(self, Bmt.command_params, **kwargs)
        Container.__init__(self)

    def __call__(self, **kwargs):
        #Need to figure out how to call container
        pass

    def __setattr__(self, name, value):
        self.__icool_setattr__(name, value)
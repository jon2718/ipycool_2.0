from modeledcommandparameter import *
from pseudoregion import *


class Refp(ModeledCommandParameter, PseudoRegion):
    """
    Reference particle
    """
    begtag = 'REFP'
    endtag = ''
    models = {

        'model_descriptor': {'desc': 'Phase model',
                             'name': 'phmodref',
                             'num_parms': 5,
                             'for001_format': {'line_splits': [5]}},

        '0_crossing':
        {'desc': '0-crossing phase iterative procedure',
         'doc': 'Uses iterative procedure to find 0-crossing phase; tracks through all regions.  Only works with ACCEL modesl 1,2 and 13.',
         'icool_model_name': 2,
         'parms':
                 {'phmodref': {'pos': 5, 'type': 'String', 'doc': ''},
                  'bmtype': {'pos': 1, 'type': 'Int', 'doc': ''}}},

        'const_v':
        {'desc': 'Assumes constant reference particle velocity',
         'doc': 'Applies to any region',
         'icool_model_name': 3,
         'parms':
                 {'phmodref': {'pos': 5, 'type': 'String', 'doc': ''},
                  'bmtype': {'pos': 1, 'type': 'Int', 'doc': ''},
                  'pz0': {'pos': 2, 'type': 'Real', 'doc': ''},
                  't0': {'pos': 3, 'type': 'Real', 'doc': ''}}},

        'en_loss':
        {'desc': 'Assumes constant reference particle velocity',
         'doc': 'Applies to any region',
         'icool_model_name': 4,
         'parms':
                 {'phmodref': {'pos': 5, 'type': 'String', 'doc': ''},
                  'bmtype': {'pos': 1, 'type': 'Int', 'doc': ''},
                  'pz0': {'pos': 2, 'type': 'Real', 'doc': ''},
                  't0': {'pos': 3, 'type': 'Real', 'doc': ''},
                  'dedz': {'pos': 4, 'type': 'Real', 'doc': ''}}},

        'delta_quad_cav':
        {'desc': 'Assumes constant reference particle velocity',
         'doc': 'Applies to any region',
         'icool_model_name': 5,
         'parms':
                 {'phmodref': {'pos': 5, 'type': 'String', 'doc': ''},
                  'bmtype': {'pos': 1, 'type': 'Int', 'doc': ''},
                  'e0': {'pos': 2, 'type': 'Real', 'doc': ''},
                  'dedz': {'pos': 3, 'type': 'Real', 'doc': ''},
                  'd2edz2': {'pos': 4, 'type': 'Real', 'doc': ''}}},

        'delta_quad_any':
        {'desc': 'Assumes constant reference particle velocity',
         'doc': 'Applies to any region',
         'icool_model_name': 6,
         'parms':
                 {'phmodref': {'pos': 5, 'type': 'String', 'doc': ''},
                  'bmtype': {'pos': 1, 'type': 'Int', 'doc': ''},
                  'e0': {'pos': 2, 'type': 'Real', 'doc': ''},
                  'dedz': {'pos': 3, 'type': 'Real', 'doc': ''},
                  'd2edz2': {'pos': 4, 'type': 'Real', 'doc': ''}}},

    }

    def __init__(self, **kwargs):
        if ModeledCommandParameter.check_command_params_init(self, Refp.models, **kwargs) is False:
            sys.exit(0)

    def __call__(self, **kwargs):
        pass

    def __setattr__(self, name, value):
        self.__modeled_command_parameter_setattr__(name, value, Refp.models)

    def __str__(self):
        pass
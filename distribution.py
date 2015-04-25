from modeledcommandparameter import *


class Distribution(ModeledCommandParameter):

    """
    A Distribution is a:
    (1) bdistyp (I) beam distribution type {1:Gaussian 2:uniform circular segment}
    (2-13) 12 Parameters for bdistyp
    """
    begtag=''
    endtag=''
    
    models = {

        'model_descriptor': {'desc': 'Distribution type',
                             'name': 'bdistyp',
                             'num_parms': 13,
                             'for001_format': {'line_splits': [1, 6, 6]}},

        'gaussian':
        {'desc': 'Gaussian beam distribution',
         'doc': '',
         'icool_model_name': 1,
         'parms':
                 {'bdistyp': {'pos': 1, 'type': 'String', 'doc': ''},
                  'x_mean': {'pos': 2, 'type': 'Real', 'doc': ''},
                  'y_mean': {'pos': 3, 'type': 'Real', 'doc': ''},
                  'z_mean': {'pos': 4, 'type': 'Real', 'doc': ''},
                  'px_mean': {'pos': 5, 'type': 'Real', 'doc': ''},
                  'py_mean': {'pos': 6, 'type': 'Real', 'doc': ''},
                  'pz_mean': {'pos': 7, 'type': 'Real', 'doc': ''},
                  'x_std': {'pos': 8, 'type': 'Real', 'doc': ''},
                  'y_std': {'pos': 9, 'type': 'Real', 'doc': ''},
                  'z_std': {'pos': 10, 'type': 'Real', 'doc': ''},
                  'px_std': {'pos': 11, 'type': 'Real', 'doc': ''},
                  'py_std': {'pos': 12, 'type': 'Real', 'doc': ''},
                  'pz_std': {'pos': 13, 'type': 'Real', 'doc': ''}}},

        'uniform':
        {'desc': 'Uniform circular segment beam distribution',
         'doc': '',
         'icool_model_name': 2,
         'parms':
                 {'bdistyp': {'pos': 1, 'type': 'String', 'doc': ''},
                  'r_low': {'pos': 2, 'type': 'Real', 'doc': ''},
                  'r_high': {'pos': 3, 'type': 'Real', 'doc': ''},
                  'phi_low': {'pos': 4, 'type': 'Real', 'doc': ''},
                  'phi_high': {'pos': 5, 'type': 'Real', 'doc': ''},
                  'z_low': {'pos': 6, 'type': 'Real', 'doc': ''},
                  'z_high': {'pos': 7, 'type': 'Real', 'doc': ''},
                  'pr_low': {'pos': 8, 'type': 'Real', 'doc': ''},
                  'pr_high': {'pos': 9, 'type': 'Real', 'doc': ''},
                  'pphi_low': {'pos': 10, 'type': 'Real', 'doc': ''},
                  'pphi_high': {'pos': 11, 'type': 'Real', 'doc': ''},
                  'pz_low': {'pos': 12, 'type': 'Real', 'doc': ''},
                  'pz_high': {'pos': 13, 'type': 'Real', 'doc': ''}}},

    }

    def __init__(self, **kwargs):
        if ModeledCommandParameter.check_command_params_init(self, Distribution.models, **kwargs) is False:
            sys.exit(0)

    def __call__(self, **kwargs):
        pass

    def __setattr__(self, name, value):
        self.__modeled_command_parameter_setattr__(name, value, Distribution.models)


    def gen_for001(self, file):
        ModeledCommandParameter.gen_for001(self, file)

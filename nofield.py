from field import *


class NoField(Field):

    """No Field"""
    begtag = 'NONE'
    endtag = ''

    models = {
        'model_descriptor': {'desc': 'Name of model parameter descriptor',
                                     'name': None,
                                     'num_parms': 15,
                                     'for001_format': {'line_splits': [15]}},
    }

    def __init__(self, **kwargs):
        if ModeledCommandParameter.check_command_params_init(self, NoField.models, **kwargs) is False:
            sys.exit(0)

    def __call__(self, **kwargs):
        pass

    def __setattr__(self, name, value):
        self.__modeled_command_parameter_setattr__(name, value, NoField.models)

    def __str__(self):
        return Field.__str__(self)

    def gen_for001(self, file):
        ModeledCommandParameter.gen_for001(self, file)
from regularregion import RegularRegion
from region import Region
from icoolobject import *


class SubRegion(RegularRegion):

    """
    A SubRegion is a:
    (1) IRREG r-region number;
    (2) RLOW Innter radius of this r subregion;
    (3) RHIGH Outer radius of this r subregion;
    (4) Field object; and
    (5) Material object.
    """
    num_params = 5
    for001_format = {'line_splits': [3, 1, 1]}

    command_params = {
        'irreg': {'desc': 'R-Region Number',
                  'doc': '',
                  'type': 'Integer',
                  'req': True,
                  'pos': 1},

        'rlow': {'desc': 'Inner radius of this r subregion',
                 'doc': '',
                 'type': 'Float',
                 'req': True,
                 'pos': 2},

        'rhigh': {'desc': 'Outer radius of this r subregion',
                  'doc': '',
                  'type': 'Float',
                  'req': True,
                  'pos': 3},

        'field': {'desc': 'Field object',
                  'doc': '',
                  'type': 'Field',
                  'req': True,
                  'pos': 4},

        'material': {'desc': 'Material object',
                     'doc': '',
                     'type': 'Material',
                     'req': True,
                     'pos': 5}
    }

    def __init__(self, **kwargs):
        ICoolObject.check_command_params_init(self, SubRegion.command_params, **kwargs)

    def __setattr__(self, name, value):
        self.__icool_setattr__(name, value, SubRegion.command_params)

    def __str__(self):
        return 'SubRegion:\n' + 'irreg=' + str(self.irreg) + '\n' + 'rlow=' + str(self.rlow) + '\n' + \
            'rhigh=' + str(self.rhigh) + '\n' + 'Field=' + \
            str(self.field) + '\n' + \
            'Material=' + str(self.material)

    def __repr__(self):
        return 'SubRegion:\n' + 'irreg=' + str(self.irreg) + '\n' + 'rlow=' + str(self.rlow) + '\n' + \
            'rhigh=' + str(self.rhigh) + '\n' + 'Field=' + \
            str(self.field) + '\n' + \
            'Material=' + str(self.material)

    def __setattr__(self, name, value):
        self.__icool_setattr__(name, value, SubRegion.command_params)


    def gen_for001(self, file):
        Region.gen_for001(self, file)
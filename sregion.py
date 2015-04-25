from regularregioncontainer import *
# from subregion import SubRegion


class SRegion(RegularRegionContainer):

    """
    SREGION - Start of new s-region. Describes field and material properties.

    Parameters:
    1.1) SLEN (R) Length of this s region [m]
    1.2) NRREG (I) # of radial subregions of this s region {1-4}
    1.3) ZSTEP (R) step for tracking particles [m]
    Note that for fixed-stepping the program may modify this value slightly to get
    an integral number of steps in the region.

    The following parameters are repeated for each r subregion:
    2.1) IRREG (I) r-region number
    2.2) RLOW (R) Inner radius of this r subregion[m]
    2.3) RHIGH (R) Outer radius of this r subregion[m]

    3) FTAG (A4) Tag identifying field in this r subregion
    (See specific field type below)

    4) FPARM (R) 15 parameters describing field (see specific field type below)
    These 15 parameters must be on one input line.

    5) MTAG (2A4) Tag identifying material composition in this r subregion
    The wedge geometry can accept a second MTAG parameter.
    The first material refers to the interior of the wedge.
    The second material, if present, refers to the exterior of the wedge.
    If a second MTAG parameter is not present, vacuum is assumed. (see specific material type below)

    6) MGEOM (A6) Tag identifying material geometry in this r subregion.
    (see specific material type below)

    7) GPARM (R) 10 Parameters describing material geometry.
    These 10 parameters must be on one input line (see specific material type below)
    """

    allowed_enclosed_commands = ['SubRegion']

    begtag = 'SREGION'
    endtag = ''
    num_params = 3
    for001_format = {'line_splits': [3]}

    command_params = {
        'slen': {
            'desc': 'Length of this s region [m]',
            'doc': '',
            'type': 'Real',
            'req': True,
            'pos': 1},
        'nrreg': {
            'desc': '# of radial subregions of this s region {1-4}',
            'doc': '',
            'type': 'Int',
            'min': 1,
            'max': 4,
            'req': True,
            'pos': 2},
        'zstep': {
            'desc': 'Step for tracking particles [m]',
            'doc': '',
            'type': 'Real',
            'req': True,
            'pos': 3},
        #'outstep': {
        #    'desc': 'Step for generating OUTPUT commands within SRegion.',
        #    'doc': 'Will wrap SRegion in REPEAT/ENDREPEAT statements.',
        #    'type': 'Real',
        #    'req': False,
        #    'pos': None}
        }

    def __init__(self, **kwargs):
        ICoolObject.check_command_params_init(self, SRegion.command_params, **kwargs)
        Container.__init__(self)

    def __setattr__(self, name, value):
        self.__icool_setattr__(name, value)

    def __str__(self):
        ret_str = 'SRegion:\n' + 'slen=' + str(self.slen) + '\n' + 'nrreg=' + str(self.nrreg) + '\n' + \
           'zstep=' + str(self.zstep) + '\n' + str(Container.__str__(self))
        return ret_str

    def __repr__(self):
        return 'SRegion:\n ' + 'slen=' + \
            str(self.slen) + '\n' + 'nrreg=' + str(self.nrreg) + \
            '\n' + 'zstep=' + str(self.zstep)

    def add_subregion(self, subregion):
        pass

    def add_subregions(self, subregion_list):
        pass

    def gen_for001(self, file):
        RegularRegionContainer.gen_for001(self, file)

# -*- coding: utf-8 -*-
import sys
import icool_exceptions as ie
import copy


"""Nomenclature:

An ICOOL input file consists of:
1. Problem title
2. General control variables
3. Beam generation variables
4. Physics interactions control variables
5. Histogram definition variables
6. Scatterplot definition variables
7. Z-history definition variables
8. R-history definition variables
9. Emittance plane definition variables
10. Covariance plane definition variables
11. Region definition variables.
** Note that region definition variables are referred to in the ICOOL Manual and
herein as commands.

This program will use of following object definitions:
Namelists.  Namelists in the for001.dat file are preceded by an '&'
sign (e.g., &cont).

Namelists include:
CONT: Control Variables
BMT: Beam Generation Variables
INTS: Phyiscs Interactions Control Variables
NHS: Histogram Definition Variables
NSC: Scatterplot definition Variables
NZH: Z-History Definition Variables
NRH: R-History Definition Variables
NEM: Emittance Plane Definition Variables
NCV: Covariance Plane Definition Variables


Namelist variables:
Each of the above namelists is associated with a respective set of variables.

Commands:
Commands comprise both Regular Region Commands and Pseudoregion Commands

Regular Region Commands:
SECTION
BEGS
REPEAT
CELL
SREGION
ENDREPEAT
ENDCELL
ENDSECTION

Psuedoregion Commands:
APERTURE
CUTV
DENP
DENS
DISP
DUMMY
DVAR
EDGE
GRID
OUTPUT
RESET
RKICK
ROTATE
TAPER
TILT
TRANSPORT
BACKGROUND
BFIELD
ENDB
!
&

Command parameters:
Each regular and pseduoregion command is respectively associated with a set of command parameters.
"""
from IPython.core.magic_arguments import (argument, magic_arguments,
                                          parse_argstring)
from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)

#@register_line_magic


@magic_arguments()
@argument('-o', '--option', help='An optional argument.')
@argument('arg', type=int, help='An integer positional argument.')
def ipycool(self, arg):
    """ A really cool ipycool magic command.

    """
    args = parse_argstring(ipycool, arg)


@magic_arguments()
@register_line_magic
def icool():
    "ICOOL"
    exec('!icool')


class ICoolGenerator(object):

    def get_base_classes(self):
        base_tuple = self.__class__.__bases__
        bases_names = tuple()
        for c in base_tuple:
            bases_names += tuple([c.__name__])
        return bases_names

    def icoolgenerate_for001(self, file):
        base_classes = self.get_base_classes()
        if 'ICoolNameList' in base_classes:
            ICoolNameList.gen_for001(self, file)
            if 'Container' in base_classes:
                Container.gen_for001(self, file)
        else:
            if 'RegularRegion' or 'PseudoRegion' in base_classes:
                Region.gen_begtag(self, file)
                Region.gen_for001(self, file)
                if 'Container' in base_classes:
                    Container.gen_for001(self, file)
                Region.gen_endtag(self, file)

    def gen_begtag(self, file):
        if hasattr(self, 'begtag'):
            file.write(self.begtag)
            file.write('\n')

    def gen_endtag(self, file):
        if hasattr(self, 'endtag'):
            file.write(self.endtag)
            file.write('\n')


class ICoolObject(object):

    """Generic ICOOL object providing methods for"""

    def __init__(self, kwargs):
        if self.check_command_params_init(kwargs) is False:
            sys.exit(0)
        else:
            self.setall(kwargs)

    def __call__(self, kwargs):
        if self.check_command_params_call(kwargs) is False:
            sys.exit(0)
        else:
            self.setall(kwargs)

    def __str__(self, return_str):
        command_parameters_dict = self.command_params
        for key in command_parameters_dict:
            if hasattr(self, key):
                return_str += '\n'
                return_str += key
                return_str += ': '
                return_str += str(getattr(self, key))
        return return_str

    def __repr__(self):
        return '[ICool Object]'

    """Checks whether all required command parameters specified in __init__ are provided are valid
    for the command.
    Valid means the parameters are recognized for the command, all required parameters are provided
    and the parameters are the correct type."""

    def __setattr__(self, name, value):
        if self.check_command_param(name):
            object.__setattr__(self, name, value)
        else:
            sys.exit(0)

    def check_command_param(self, command_param):
        """
        Checks whether a parameter specified for command is valid.
        """
        command_parameters_dict = self.get_command_params()
        # Check command parameters are all valid
        try:
            if command_param not in command_parameters_dict:
                raise ie.InvalidCommandParameter(
                    command_param,
                    command_parameters_dict.keys())
        except ie.InvalidCommandParameter as e:
            print e
            return False
        except ie.InvalidType as e:
            print e
            return False
        return True

    def check_command_params_valid(
            self,
            command_params,
            command_parameters_dict):
        """Returns True if command_params are valid (correspond to the command)
        Otherwise raises an exception and returns False"""
        # command_parameters_dict = self.get_command_params()
        try:
            for key in command_params:
                if key not in command_parameters_dict:
                    raise ie.InvalidCommandParameter(
                        key,
                        command_parameters_dict)
        except ie.InvalidCommandParameter as e:
            print e
            return False
        return True

    def check_all_required_command_params_specified(
            self,
            command_params,
            command_parameters_dict):
        """Returns True if all required command parameters were specified
        Otherwise raises an exception and returns False"""
        # command_parameters_dict = self.get_command_params()
        try:
            for key in command_parameters_dict:
                if self.is_required(key, command_parameters_dict):
                    if key not in command_params:
                        raise ie.MissingCommandParameter(key, command_params)
        except ie.MissingCommandParameter as e:
            print e
            return False
        return True

    def check_command_params_type(self, command_params, command_params_dict):
        """Checks to see whether all required command parameters specified were of the correct type"""
        # command_params_dict = self.get_command_params()
        try:
            for key in command_params:
                if self.check_type(
                        command_params_dict[key]['type'],
                        command_params[key]) is False:
                    raise ie.InvalidType(
                        command_params_dict[key]['type'],
                        command_params[key].__class__.__name__)
        except ie.InvalidType as e:
            print e
            return False
        return True

    def check_command_param_type(self, name, value):
        """Checks to see whether a particular command parameter of name with value is of the correct type"""
        command_params_dict = self.get_command_params()
        try:
            if self.check_type(
                    command_params_dict[name]['type'],
                    value) is False:
                raise ie.InvalidType(
                    command_params_dict[name]['type'],
                    value.__class__.__name__)
        except ie.InvalidType as e:
            print e
            return False
        return True

    def check_command_params_init(self, command_params):
        """
        Checks whether the parameters specified for command are valid, all required parameters are
        specified and all parameters are of correct type.  If not, raises an exception.
        """
        command_parameters_dict = self.get_command_params()
        check_params = not self.check_command_params_valid(
            command_params,
            command_parameters_dict) or not self.check_all_required_command_params_specified(
            command_params,
            command_parameters_dict) or not self.check_command_params_type(
            command_params,
            command_parameters_dict)

        if check_params:
            return False
        else:
            return True

    def check_command_params_call(self, command_params):
        """
        Checks whether the parameters specified for command are valid and all required parameters exist.
        """
        command_parameters_dict = self.get_command_params()
        return self.check_command_params_valid(command_params, command_parameters_dict) and\
            self.check_command_params_type(
            command_params,
            command_parameters_dict)

    def setall(self, command_params):
        for key in command_params:
            self.__setattr__(key, command_params[key])

    def setdefault(self, command_params):
        command_params_dict = self.get_command_params()
        for key in command_params_dict:
            if key not in command_params:
                self.__setattr__(key, command_params_dict[key]['default'])

    def check_type(self, icool_type, provided_type):
        """Takes provided python object and compares with required icool type name.
        Returns True if the types match and False otherwise.
        """
        provided_type_name = provided_type.__class__.__name__
        print icool_type, provided_type_name
        if icool_type == 'Real':
            if provided_type_name == 'int' or provided_type_name == 'long' or provided_type_name == 'float':
                return True
            else:
                return False

        if icool_type == 'Integer':
            if provided_type_name == 'int' or provided_type_name == 'long':
                return True
            else:
                return False

        if icool_type == 'Logical':
            if provided_type_name == 'bool':
                return True
            else:
                return False

        if icool_type == 'Field':
            if isinstance(provided_type, Field):
                return True
            else:
                return False

        if icool_type == 'Material':
            if isinstance(provided_type, Material):
                return True
            else:
                return False

        if icool_type == 'SubRegion':
            if isinstance(provided_type, SubRegion):
                return True
            else:
                return False

        if icool_type == 'Distribution':
            if isinstance(provided_type, Distribution):
                return True
            else:
                return False

        if icool_type == 'Correlation':
            if isinstance(provided_type, Correlation):
                return True
            else:
                return False

    def get_command_params(self):
        return self.command_params

    def is_required(self, command_param, command_parameters_dict):
        # command_parameters_dict = self.get_command_params()
        if 'req' not in command_parameters_dict[command_param]:
            return True
        else:
            return command_parameters_dict[command_param]['req']

    def gen_parm(self):
        command_params = self.get_command_params()
        #parm = [None] * len(command_params)
        parm = [None] * self.num_params
        for key in command_params:
            pos = int(command_params[key]['pos']) - 1
            val = getattr(self, key)
            parm[pos] = val
        print parm
        return parm

    def for001_str_gen(self, value):
        if value.__class__.__name__ == 'bool':
            if value is True:
                return '.true.'
            else:
                return '.false.'
        else:
            return str(value)

    def get_begtag(self):
        return self.begtag

    def get_endtag(self):
        return self.endtag

    def get_line_splits(self):
        return self.for001_format['line_splits']


class ICoolNameList(ICoolObject):

    def gen_for001(self, file):
        name = self.__class__.__name__.lower()
        file.write('&')
        file.write(name)
        file.write(' ')
        count = 0
        items_per_line = 5
        for key in self.command_params:
            if hasattr(self, key):
                file.write(str(key))
                file.write('=')
                file.write(self.for001_str_gen(getattr(self, key)))
                file.write(' ')
                count = count + 1
                if count % items_per_line == 0:
                    file.write('\n')
        file.write('/')
        file.write('\n')


class Container(ICoolObject):

    """Abstract class container for other commands.
    """

    def __init__(self, enclosed_commands=None):
        if enclosed_commands is None:
            print "Setting self.enclosed_commands to []"
            self.enclosed_commands = []
        else:
            if self.check_allowed_enclosed_commands(enclosed_commands):
                self.enclosed_commands = enclosed_commands

    def __setattr__(self, name, value):
        # command_parameters_dict = self.command_params
        if name == 'enclosed_commands':
            object.__setattr__(self, name, value)
        else:
            if not self.check_command_param(name):
                return False
            else:
                if not self.check_command_param_type(name, value):
                    return False
                else:
                    object.__setattr__(self, name, value)
                    return True

    def __str__(self):
        ret_str = ''
        for command in self.enclosed_commands:
            ret_str += str(command)
        return ret_str

    def add_enclosed_command(self, command):
        if self.check_allowed_enclosed_command(command) is False:
            sys.exit(0)
        else:
            self.enclosed_commands.append(command)

    def insert_enclosed_command(self, command, insert_point):
        if self.check_allowed_command(command) is False:
            sys.exit(0)
        else:
            self.enclosed_commands.insert(insert_point, command)

    def remove_enclosed_command(self, delete_point):
        del self.enclosed_commands[delete_point]

    def check_allowed_enclosed_command(self, command):
        try:
            if command.__class__.__name__ not in self.allowed_enclosed_commands:
                raise ie.ContainerCommandError(
                    command,
                    self.allowed_enclosed_commands)
        except ie.ContainerCommandError as e:
            print e
            return False
        return True

    def check_allowed_enclosed_commands(self, enclosed_commands):
        pass

    def gen_for001(self, file):
        for command in self.enclosed_commands:
            print 'Command is: ', command
            if hasattr(command, 'gen_for001'):
                command.gen_for001(file)
            else:
                file.write(self.for001_str_gen(command))


class ICoolNameListContainer(ICoolNameList, Container):

    def gen_for001(self, file):
        ICoolNameList.gen_for001(self, file)
        Container.gen_for001(self, file)


class Title(ICoolObject):
    command_params = {
        'title': {'desc': 'Title of ICOOL simulation',
                  'doc': '',
                  'type': 'String',
                  'req': True,
                  'default': None}

    }

    def __init__(self, title):
        self.title = title

    def __str__(self):
        return 'Problem Title: ' + self.title + '\n'

    def __repr__(self):
        return 'Problem Title: ' + self.title + '\n'

    def gen_for001(self, file):
        file.write(self.title)
        file.write('\n')


class Cont(ICoolNameList):
    command_params = {
        'betaperp': {
            'desc': '(R) beta value to use in calculating amplitude variable A^2', 'doc': '',
            'type': 'Real',
            'req': False,
            'default': None},
        'bgen': {
            'desc': '(L) if .true.=>generate initial beam particles, otherwise read input from FOR003.DAT (true)',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': True},
        'bunchcut': {
            'desc': '(R) maximum time difference allowed between a particle and the reference particle [s] (1E6)',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 1E6},
        'bzfldprd': {
            'desc': '(R) Bz for solenoid at location of production plane (0.) This is used for output to '
                    'file for009.dat and for canonical angular momentum correction.',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': None},
        'dectrk': {
            'desc': '(L) if .true. => continue tracking daughter particle following decay.',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': False},
        'diagref': {
            'desc': '(L) if .true. => continue tracking daughter particle following decay.',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': False},
        'epsf': {
            'desc': '(R) desired tolerance on fractional field variation, energy loss, and multiple '
                    'scattering per step',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 0.05},
        'bzfldprd': {
            'desc': '(R) Bz for solenoid at location of production plane (0.) This is used for output to '
                    'file for009.dat and for canonical angular '
                    'momentum correction.',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': None},
        'dectrk': {
            'desc': '(L) if .true. => continue tracking daughter particle following decay',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': False},
        'diagref': {
            'desc': '(L) if .true. => continue tracking daughter particle following decay',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': False},
        'epsf': {
            'desc': '(R) desired tolerance on fractional field variation, energy loss, and multiple '
                    'scattering per step',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': False},
        'epsreq': {
            'desc': '(R) required tolerance on error in tracking parameters (1E-3) This parameter is '
                    'only used if varstep = true',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': None},
        'epsstep': {
            'desc': '(R) desired tolerance in spatial stepping to reach each destination plane [m]',
            'type': 'Real',
            'doc': '',
            'req': False,
            'default': 1E-6},
        'ffcr': {
            'desc': '(L) if .true. => inserts form feed and carriage returns in the output log file so there '
                    'are two plots per page starting at the top of a page',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': False},
        'forcerp': {
            'desc': '(L) if .true. => set x, y, Px, and Py for reference particle to 0 for each new REFP '
                    'command and for each ACCEL region with phasemodel=4.',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': True},
        'fsav': {
            'desc': '(L) if .true. => store particle info at plane IZFILE into file FOR004.DAT. (false). '
                    'It is possible to get the initial distribution of particles that get a given error flag be '
                    'setting the plane=IFAIL . It is possible to get the initial distribution of particles that '
                    'successfully make it to the end of the simulation by setting the plane= -1.',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': None},
        'fsavset': {
            'desc': '(L) if .true. => modify data stored using FSAV in FOR004.DAT to have z=0 and '
                    'times relative to reference particle at plane IZFILE.',
            'doc': '',
            'type':
            'Logical',
            'req': False,
            'default': False},
        'f9dp': {
            'desc': '(I) number of digits after the decimal point for floating point variables in FOR009.DAT '
                    '{4,6,8,10,12,14,16,17} (4) F9DP=17 gives 16 digits after the decimal point and 3 digits in the '
                    'exponent',
            'doc': '',
            'type': 'Integer',
            'req': False,
            'default': None},
        'goodtrack': {
            'desc': '(L) if .true. and BGEN=.false. => only accepts input data from file FOR003.DAT if '
                    'IPFLG=0.; if .false. => resets IPFLG of bad input tracks to 0 (this allows processing a '
                    'file of bad tracks for diagnostic purposes)',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': True},
        'izfile': {
            'desc': '(I) z-plane where particle info is desired when using FSAV. Use 1 to store beam at '
                    'production. Saves initial particle properties for bad tracks if IZFILE=IFAIL #.  Saves initial '
                    'particle properties for tracks that get to the end of the simulation if IZFILE=-1.  IZFILE '
                    'should point to the end of a REGION or to an APERTURE , ROTATE or TRANSPORT pseudoregion '
                    'command.',
            'doc': '',
            'type': 'Integer',
            'req': False,
            'default': None},
        'magconf': {
            'desc': '(I) if 19 < MAGCONF=mn < 100 => reads in file FOR0mn.DAT, which contains data on '
            'solenoidal magnets. Used with SHEET, model 4.',
            'doc': '',
            'type': 'Integer',
            'req': False,
            'default': 0},
        'mapdef': {
            'desc': '(I) if 19 < MAPDEF=mn < 100 => reads in file FOR0mn.DAT, which contains data on how '
                    'to set up field grid. Used with SHEET, model 4.',
            'doc': '',
            'type': 'Integer',
            'req': False,
            'default': 0},
        'neighbor': {
            'desc': "(L) if .true. => include fields from previous and following regions when calculating "
                    "field.  This parameter can be used with soft-edge fields when the magnitude of the "
                    "field doesn't fall to 0 at the region boundary. A maximum of 100 region can be used "
                    "with this feature.",
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': False},
        'neutrino': {
            'desc': '(I) if 19 < NEUTRINO=mn < 100 => writes out file FOR0mn.DAT, which contains '
                    'neutrino production data. See section 5.2 for the format.',
            'doc': '',
            'type': 'Integer',
            'req': False,
            'default': 0},
        'nnudk': {
            'desc': '(I) # of neutrinos to produce at each muon, pion and kaon decay.',
            'doc': '',
            'type': 'Integer',
            'req': False,
            'default': 1},
        'npart': {
            'desc': '(I) # of particles in simulation. The first 300,000 particles are stored in memory. '
                    'Larger numbers are allowed in principle since ICOOL writes the excess particle '
                    'information to disc. However, there can be a large space and speed penalty in doing '
                    'so.',
            'doc': '',
            'type': 'Integer',
            'req': False,
            'default': None},
        'nprnt': {
            'desc': ' Number of diagnostic events to print out to log file.',
            'doc': '',
            'type': 'Integer',
            'req': False,
            'default': -1},
        'npskip': {
            'desc': 'Number of input particles in external beam file to skip before processing starts',
            'doc': '',
            'type': 'Integer',
            'req': False,
            'default': 0},
        'nsections': {
            'desc': '(I) # of times to repeat basic cooling section (1).  This parameter can be used to '
                    'repeat all the commands between the SECTION and ENDSECTION commands in the problem '
                    'definition. If a REFP command immediately follows the SECTION command, it is not '
                    'repeated',
            'doc': '',
            'type': 'Integer',
            'req': False,
            'default': 1},
        'ntuple': {
            'desc': '(L) if .true. => store information about each particle after every region in file '
                    'FOR009.DAT. This variable is forced to be false if RTUPLE= true.(false)}',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': False},
        'nuthmin': {
            'desc': '(R) Minimum polar angle to write neutrino production data to file. [radians]',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 0},
        'nuthmax': {
            'desc': 'Maximum polar angle to write neutrino production data to file. [radians]',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 3.14},
        'output1': {
            'desc': 'if .true. => write particle information at production (plane 1) to the '
                    'postprocessor output file for009.dat.',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': False},
        'phantom': {
            'desc': 'if .true. => force particle to keep initial transverse coordinates after every '
                    '(L) if .true. => force particle to keep initial transverse coordinates after '
                    'every step. This is useful for making magnetic field maps. (false)',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': False},
        'phasemodel': {
            'desc': 'PHASEMODEL (I) controls how the phase is determined in rf cavities. (1) '
                    '1: takes phase directly from ACCEL command [degrees] '
                    '2 - 6: takes phase model from REFP command '
                    '7: reads phases in from file FOR0mn.DAT, where RFPHASE=mn. See sec. 5.1.},',
            'doc': '',
            'type': 'Integer',
            'req': False,
            'default': 1},
        'prlevel': {
            'desc': 'Controls level of print information to log file (for NPRINT events);higher # '
                    'gives more print(1)',
            'doc': '1: values at end of region '
                   '2: + values at end of each time step '
                   '3: + E,B values at each step '
                   '4: + information in cylindrical coordinates',
            'type': 'Integer',
            'req': False,
            'default': 1,
            'min': 1,
            'max': 4},
        'prnmax': {
            'desc': 'Sets maximum number of steps to generate print out inside a region',
            'doc': '',
            'type': 'Integer',
            'req': False,
            'default': 300},
        'pzmintrk': {
            'desc': 'Sets the value of Pz below which tracking stops. [GeV/c]',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 0.001},
        'rfdiag': {
            'desc': 'if 19 < RFDIAG=mn < 100 => writes rf diagnostic information at the '
                    'end of each accelerator region to file FOR0mn.DAT.',
            'doc': '',
            'type': 'Integer',
            'req': False,
            'default': 0,
            'min': 19,
            'max': 100},
        'rfphase': {
            'desc': 'If PHASEMODEL=5 => reads rf phases, frequencies and gradients '
                    'for the cavities from file FOR0mn.DAT, where RFPHASE=mn '
                    'and 19 < mn < 100 (0)',
            'doc': '',
            'type': 'Integer',
            'req': False,
            'default': 0,
            'min': 19,
            'max': 100},
        'rnseed': {
            'desc': 'Random number seed (-1) Set to a negative integer',
            'doc': '',
            'type': 'Integer',
            'req': False,
            'default': -1},
        'rtuple': {
            'desc': 'If .true. => particle information in file FOR009.DAT is generated after '
                    'every RTUPLEN steps.',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': False},
        'rtuplen': {
            'desc': '# of steps to skip between RTUPLE generated outputs',
            'doc': '',
            'type': 'Integer',
            'req': False,
            'default': 5},
        'run_env': {
            'desc': 'If true => run ICOOL in beam envelope mode, i.e. no tracking',
            'doc': 'For solenoidal channels only.',
            'type': 'Logical',
            'req': False,
            'default': False},
        'scalestep': {
            'desc': 'Factor that modifies all step sizes in a problem simultaneously.',
            'doc': 'Only works in fixed stepsize mode.',
            'type': 'Real',
            'req': False,
            'default': 1.0},
        'spin': {
            'desc': 'If .true. => include calculation of polarization',
            'doc': '',
            'type':
            'Logical',
            'req': False,
            'default': False},
        'spinmatter': {
            'desc': 'Controls whether muon depolarization effects in matter are simulated',
            'doc': '0: no depolarization simulation '
                   '1: depolarization simulation using Rossmanith model'
                   '2: depolarization simulation using spin flip probabilities',
            'type': 'Integer',
            'req': False,
            'default': 0,
            'min': 0,
            'max': 3},
        'spintrk': {
            'desc': 'Controls whether spin variables are tracked',
            'doc': '0: no spin tracking '
                   '1: track spin in muon rest frame using BMT equations',
            'type': 'Integer',
            'req': False,
            'default': 0,
            'min': 0,
            'max': 1},
        'stepmax': {
            'desc': 'maximum step size that can be used for variable stepping [m]',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 1},
        'stepmin': {
            'desc': 'minimum step size that can be used for variable stepping [m]',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 1E-5},
        'steprk': {
            'desc': 'If .true. => use 4th order Runge-Kutta integrator for tracking. '
                    'Otherwise it uses the Boris push method in straight regions',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': True},
        'summary': {
            'desc': 'if true => writes region summary table to for007.dat',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': True},
        'termout': {
            'desc': 'If .true. => write output to terminal screen',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': True},
        'timelim': {
            'desc': 'Time limit for simulation [min]',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 1E9},
        'varstep': {
            'desc': 'If .true. => use adaptive step size; otherwise use fixed step ZSTEP '
                    '(until reaching the last step in a region).',
            'doc': 'This variable is forced to be false (1) in wedge material '
                   'regions, (2) when the number of radial regions is greater than 1, and (3) when '
                   'PHASEMODEL=2.',
            'type': 'Logical',
            'req': False,
            'default': True}}

    def __init__(self, **kwargs):
        ICoolObject.__init__(self, kwargs)

    def __str__(self):
        return ICoolObject.__str__(self, 'CONT')

    def __repr__(self):
        return '[Control variables: ]'

    def gen(self, file):
        ICoolObject.gen(self, file)


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
        ICoolObject.__init__(self, kwargs)
        Container.__init__(self)

    def __setattr__(self, name, value):
        Container.__setattr__(self, name, value)


class Ints(ICoolNameList):
    command_params = {
        'ldedx': {
            'desc': 'If .true. => simulate mean ionization energy loss dE/dx (true)',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': True},
        'lscatter': {
            'desc': 'if .true. => simulate multiple scattering',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': True},
        'lstrag': {
            'desc': 'If .true. => simulate energy straggling',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': True},
        'ldecay': {
            'desc': 'If .true. => simulate particle decays',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': True},
        'ldray': {
            'desc': 'If .true. => simulate discrete energy loss from delta rays',
            'doc': 'When LDRAY is true, the program forces the parameters DELEV=2 and STRAGLEV=5.',
            'type': 'Logical',
            'req': False,
            'default': True},
        'linteract': {
            'desc': 'If .true. => simulate inelastic nuclear interactions of pions, kaons and protons',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': False},
        'lspace': {
            'desc': 'If .true. => consider effects of space charge',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': False},
        'lelms': {
            'desc': 'If .true. => use ELMS model2 for energy loss and scattering',
            'doc': 'When this command is true an external file ELMSCOM.TXT must be provided. '
            'This file consists of two lines giving (1) the ELMS run directory including path '
            'and (2) the root part of the path name to the ELMS database files. For example, '
            '\muon\elmsdb\rundirectory.txt\n'
            '\muon\elmsdb\elmsfv3run\n'
            'ELMS only works in regions containing hydrogen (the SCATLEV model is used in other '
            'regions). '
            'For hydrogen regions use a stepsize around 5 mm for maximum accuracy. A stepsize of '
            '1 mm gives significantly worse results.',
            'type': 'Logical',
            'req': False,
            'default': False},
        'lsamcs': {
            'desc': 'If .true. => use SAMCS model3 of correlated straggling and scattering',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': False},
        'delev': {
            'desc': 'Model level for dEdx (2)',
            'doc': '1: Bethe-Bloch\n'
            '2: Bethe-Bloch with density effect\n'
            '3: restricted Bethe-Bloch with density effect\n'
            '4: test mode with dE = const * dz, independent of velocity and angle',
            'type': 'Integer',
            'req': False,
            'default': 2,
            'min': 1,
            'max': 4},
        'scatlev': {
            'desc': '(I) model level for multiple scattering',
            'doc': '1: Gaussian( 0, Rossi-Greisen )\n'
            '2: Gaussian( 0, Highland )\n'
            '3: Gaussian( 0, Lynch-Dahl )\n'
            '4: Bethe version of Moliere distribution (with Rutherford limit)\n'
            '5: Rutherford\n'
            '6: Fano (with Rutherford limit)\n'
            '7: Tollestrup (with Rutherford limit)\n'
            'Level 2 contains a logarithm term in computing the Gaussian width, so\n'
            'it is not useful for general monte carlo work. It gives an accurate estimate of\n'
            'the width of the distribution when the step size is the same as the region size.\n'
            'In models 4, 6, and 7 when the effective number of scatters is less than 20 Rutherford\n'
            'scattering is used with the actual number of scatters in a given step taken from a\n'
            'Poisson distribution.',
            'type': 'Integer',
            'req': False,
            'default': 6,
            'min': 1,
            'max': 6},
        'straglev': {
            'desc': '(I) Model level for straggling ',
            'doc': '1: Gaussian( Bohr )\n'
            '2: Landau distribution\n'
            '3: (not used)\n'
            '4: Vavilov distribution (with appropriate Landau and Gaussian limits determined '
            'by the program)\n'
            '5: restricted energy fluctuations from continuous processes with energy below DCUTx.',
            'type': 'Integer',
            'req': False,
            'default': 4,
            'min': 1,
            'max': 5},
        'declev': {
            'desc': '(I) model level for particle decays (1)',
            'doc': '1: uniform polar decay angle for daughter particle in parent rest frame\n'
            '2: 90 degree polar decay angle for daughter particle in parent rest frame\n'
            '3: uniform polar decay angle for daughter particle in parent rest frame; '
            'no mu-->e decays.\n'
            '4: 90 degree polar decay angle for daughter particle in parent rest frame; '
            'no mu->e decays\n'
            '5: uniform polar decay angle for daughter particle in parent rest frame; '
            'no mu-->e decays;\n'
            'save accumulated fractional decay length in POL(1).',
            'type': 'Integer',
            'req': False,
            'default': 1,
            'min': 1,
            'max': 5},
        'intlev': {
            'desc': 'Model level for nuclear interactions (1)',
            'doc': '1: stop tracking after an interaction\n'
            '2: stop tracking after an interaction, except for protons which generate '
            'a pion from the Wang distribution.',
            'type': 'Integer',
            'req': False,
            'default': 1,
            'min': 1,
            'max': 2},
        'spacelev': {
            'desc': 'Model level for space charge (3)',
            'doc': '1: image charge of moving bunch in cylindrical, metallic can\n'
            '2: crude transverse space charge for free space applied to all regions\n'
            '3: Gaussian bunch space charge (transverse and longitudinal) for free space '
            'applied to all regions\n'
            '4: same as model 3 for single bunch in a bunch train. All the particles are '
            'superimposed\n'
            'on 1 bunch given by parameter FRFBUNSC. Adjust PARBUNSC accordingly.',
            'type': 'Integer',
            'req': False,
            'default': 3,
            'min': 1,
            'max': 4},
        'dcute': {
            'desc': 'Kinetic energy of electrons, above which delta rays are discretely '
            'simulated [GeV] ',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 0.003},
        'dcutm': {
            'desc': 'Kinetic energy of muons and other heavy particles, above which delta '
            'rays are discretely simulated [GeV] ',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 0.003},
        'elmscor': {
            'desc': 'ELMS correlation ',
            'doc': '0: run ELMS without correlations (0)\n'
            '1: run ELMS with correlations',
            'type': 'Integer',
            'req': False,
            'default': 0,
            'min': 0,
            'max': 1},
        'facfms': {
            'desc': 'Factor to correct the Z(Z+1) term in the characteristic angle squared '
            'χC2 in Moliere multiple scattering theory '
            'times relative to reference particle at plane IZFILE.',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 1.0},
        'facmms': {
            'desc': 'Factor to correct screening angle squared χA2 in Moliere multiple ',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 1.0},
        'fastdecay': {
            'desc': 'If true => use unphysical decay constants to make {μ,π,K} decay immediately. ',
            'doc': '',
            'type': 'Logical',
            'req': False,
            'default': False},
        'frfbunsc': {
            'desc': '(R) RF frequency used for space charge model 4. [MHz] (201.) ',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 201},
        'parbunsc': {
            'desc': 'Number of muons per bunch for space charge calculation ',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 4E12},
        'pdelev4': {
            'desc': 'Momentum for DELEV=4 calculation',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 0.200},
        'wanga': {
            'desc': 'Wang parameter A ',
            'doc': 'The Wang distribution is given by '
            'd2σ/dp dΩ = A pMAX x (1-x) exp{-BxC – DpT} where x = pL / pMAX',
            'type': 'Real',
            'req': False,
            'default': 90.1},
        'wangb': {
            'desc': 'Wang parameter B',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 3.35},
        'wangc': {
            'desc': 'Wang parameter C',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 1.22},
        'wangd': {
            'desc': 'Wang parameter D',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 4.66},
        'wangpmx': {
            'desc': 'Wang parameter pMAX (1.500) The sign of this quantity is used to select '
            'π+ or π- production.',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 1.5},
        'wangfmx': {
            'desc': 'The maximum value of the Wang differential cross section',
            'doc': '',
            'type': 'Real',
            'req': False,
            'default': 13.706},
    }

    def __init__(self, **kwargs):
        ICoolObject.__init__(self, kwargs)


class Nhs(ICoolNameListContainer):
    allowed_enclosed_commands = []

    command_params = {}

    def __init__(self, **kwargs):
        ICoolObject.__init__(self, kwargs)
        Container.__init__(self)

    def __setattr__(self, name, value):
        Container.__setattr__(self, name, value)


class Nsc(ICoolNameListContainer):
    allowed_enclosed_commands = []

    command_params = {}

    def __init__(self, **kwargs):
        ICoolObject.__init__(self, kwargs)
        Container.__init__(self)

    def __setattr__(self, name, value):
        Container.__setattr__(self, name, value)


class Nzh(ICoolNameListContainer):
    allowed_enclosed_commands = []

    command_params = {}

    def __init__(self, **kwargs):
        ICoolObject.__init__(self, kwargs)
        Container.__init__(self)

    def __setattr__(self, name, value):
        Container.__setattr__(self, name, value)


class Nrh(ICoolNameListContainer):
    allowed_enclosed_commands = []

    command_params = {}

    def __init__(self, **kwargs):
        ICoolObject.__init__(self, kwargs)
        Container.__init__(self)

    def __setattr__(self, name, value):
        Container.__setattr__(self, name, value)


class Nem(ICoolNameListContainer):
    allowed_enclosed_commands = []

    command_params = {}

    def __init__(self, **kwargs):
        ICoolObject.__init__(self, kwargs)
        Container.__init__(self)

    def __setattr__(self, name, value):
        Container.__setattr__(self, name, value)


class Ncv(ICoolNameListContainer):
    allowed_enclosed_commands = []

    command_params = {}

    def __init__(self, **kwargs):
        ICoolObject.__init__(self, kwargs)
        Container.__init__(self)

    def __setattr__(self, name, value):
        Container.__setattr__(self, name, value)


class Region(ICoolObject):

    def __init__(self, kwargs):
        ICoolObject.__init__(self, kwargs)

    def __call__(self, **kwargs):
        ICoolObject.__call__(self, kwargs)

    def __str__(self):
        return '[A Region can be either a RegularRegion or PseudoRegion.]'

    def __repr__(self):
        return '[A Region can be either a RegularRegion or PseudoRegion.]'

    def __setattr__(self, name, value):
        ICoolObject.__setattr__(self, name, value)

    def gen_for001(self, file):
        if hasattr(self, 'begtag'):
            print 'Writing begtag'
            file.write(self.get_begtag())
            file.write('\n')
        parm = self.gen_parm()
        splits = self.get_line_splits()
        count = 0
        split_num = 0
        cur_split = splits[split_num]
        for command in parm:
            if count == cur_split:
                file.write('\n')
                count = 0
                split_num = split_num + 1
                cur_split = splits[split_num]
            print 'Command is: ', command
            if hasattr(command, 'gen_for001'):
                command.gen_for001(file)
            else:
                file.write(self.for001_str_gen(command))
            file.write(' ')
            count = count + 1
        file.write('\n')


class RegularRegion(Region):

    """
    RegularRegion commands include: SECTION, BEGS, REPEAT, CELL, SREGION, ENDREPEAT, ENDCELL,
    and ENDCELL.
    """

    def __init__(self, kwargs):
        Region.__init__(self, kwargs)

    def __str__(self):
        return '[A RegularRegion can be either a SECTION, BEGS, REPEAT, CELL, SREGION, ENDREPEAT, ENDCELL,\
or ENDCELL.]'

    def __repr__(self):
        return '[A RegularRegion can be either a SECTION, BEGS, REPEAT, CELL, SREGION, ENDREPEAT, ENDCELL,\
                or ENDCELL.]'


class PseudoRegion(Region):

    """
    PseudoRegion commands include: APERTURE, CUTV, DENP, DENS, DISP, DUMMY, DVAR, EDGE, GRID
    OUTPUT, REFP, REF2, RESET, RKICK, ROTATE, TAPER, TILT, TRANSPORT, BACKGROUND, BFIELD, ENDB, ! or &
    """

    def __init__(self, kwargs):
        Region.__init__(self, kwargs)

    def __str__(self):
        return '[A PseudoRegion can be either a APERTURE, CUTV, DENP, DENS, DISP, DUMMY, DVAR, EDGE, GRID\
                OUTPUT, REFP, REF2, RESET, RKICK, ROTATE, TAPER, TILT, TRANSPORT, BACKGROUND, BFIELD, ENDB, ! or &]'

    def __repr__(self):
        return '[A PseudoRegion can be either a APERTURE, CUTV, DENP, DENS, DISP, DUMMY, DVAR, EDGE, GRID\
                OUTPUT, REFP, REF2, RESET, RKICK, ROTATE, TAPER, TILT, TRANSPORT, BACKGROUND, BFIELD, ENDB, ! or &]'


class RegularRegionContainer(RegularRegion, Container):

    def gen_for001(self, file):
        # self.gen_begtag(file)
        # if hasattr(self, 'begtag'):
        #    print 'Writing begtag'
        #    file.write(self.get_begtag())
        #    file.write('\n')
        Region.gen_for001(self, file)
        Container.gen_for001(self, file)
        # self.gen_endtag(file)
        if hasattr(self, 'endtag'):
            file.write(self.get_endtag())
            file.write('\n')


class Section(RegularRegionContainer):

    """
    SECTION Start of cooling section region definition.
    The data must end with an ENDSECTION.   It can enclose any number of other commands.
    If it is desired to repeat the section definitions, the control variable NSECTIONS should be
    set >1 and a BEGS command is used to define where to start repeating.
    """

    begtag = 'SECTION'
    endtag = 'ENDSECTION'
    num_params = 0
    for001_format = {'line_splits': [0]}

    allowed_enclosed_commands = [
        'Begs',
        'Repeat',
        'Cell',
        'Background',
        'SRegion',
        'Aperture',
        'Cutv',
        'Dens',
        'Disp',
        'Dummy',
        'DVar',
        'Edge',
        'Output',
        'Refp',
        'Ref2',
        'Reset',
        'RKick',
        'Rotate',
        'Tilt',
        'Transport',
        'Comment'
        'Repeat']

    command_params = {

    }

    def __init__(self, **kwargs):
        RegularRegion.__init__(self, kwargs)
        Container.__init__(self)

    def __setattr__(self, name, value):
        Container.__setattr__(self, name, value)

    def __str__(self):
        return_str = 'SECTION\n'
        return_str += str(Container.__str__(self))
        return_str += 'END_SECTION\n'
        return return_str

    def __repr__(self):
        return 'Section\n'


class Begs(RegularRegion):

    def __init__(self):
        RegularRegion.__init(self, None, None)

    def gen(self, file):
        file.write('\n')
        file.write('BEGS')


class Repeat(RegularRegionContainer):

    """
    Start of a repeating group of region commands; the data must end with an ENDREPEAT
    command. This can be used to repeat regions inside a cell. The repeat loop can enclose any
    number of {SREGION, APERTURE, DENS, DISP, DUMMY, DVAR, EDGE, OUTPUT, REFP, REF2, RESET, RKICK,
    ROTATE, TILT, TRANSPORT} commands. Repeat sections cannot be nested in other repeat sections.
    (see parameters below)
    """
    begtag = 'REPEAT'
    endtag = 'ENDREPEAT'
    num_params = 1
    for001_format = {'line_splits': [1]}

    optional_params = {    #Not implemented yet

     'enclosed': {'desc': 'Enclosed commands',
                  'doc': 'Must be one of allowed_enclosed_commands',
                  'type': ''}

    }

    command_params = {
        'nrep': {'desc': '# of times to repeat following region commands',
                 'doc': '',
                 'type': 'Integer',
                 'req': True,
                 'pos': 1}
    }

    allowed_enclosed_commands = [
        'SRegion',
        'Aperture',
        'Dens',
        'Disp',
        'Dummy',
        'Dvar',
        'Edge',
        'Output',
        'Refp',
        'Ref2',
        'Reset',
        'Rkick',
        'Rotate',
        'Tilt',
        'Transport']

    # Used to add wrapped SRegion object. Will wrap object SRegion in Repeat with nrep = slen/outstep and generate
    # a new SRegion With slen=outstep.  Need to implement exception handling for types.
    @classmethod
    def wrapped_sreg(cls, **kwargs):
        sreg = kwargs['sreg']
        outstep = kwargs['outstep']
        sreg_copy = copy.deepcopy(sreg)
        nrep = int(sreg.slen/outstep)
        sreg_copy.slen = outstep
        r = cls(nrep=nrep)
        output = Output()
        r.add_enclosed_command(output)
        r.add_enclosed_command(sreg_copy)
        return r

    def __init__(self, **kwargs):
        RegularRegion.__init__(self, kwargs)
        Container.__init__(self)

    def __setattr__(self, name, value):
        Container.__setattr__(self, name, value)

    def __str__(self):
        return_str = 'REPEAT\n' + str(Container.__str__(self)) + 'ENDREPEAT\n'
        return return_str

    def __repr__(self):
        return 'Repeat\n'

    def gen(self, file):
        file.write('REPEAT')
        Container.gen(self, file)
        file.write('ENDREPEAT')
        file.write('/n')


class Background(PseudoRegion):

    def __init__(self, name=None, metadata=None):
        PseudoRegion.__init__(self, name, metadata)


class Bfield(PseudoRegion):

    def __init__(self, name=None, metadata=None):
        PseudoRegion.__init__(self, name, metadata)


class Edge(PseudoRegion):

    """EDGE Fringe field and other kicks for hard-edged field models
    1) edge type (A4) {SOL, DIP, HDIP, DIP3, QUAD, SQUA, SEX, BSOL, FACE}

    2.1) model # (I) {1}
    2.2-5) p1, p2, p3,p4 (R) model-dependent parameters

    Edge type = SOL
    p1: BS [T]
    If the main solenoid field is B, use p1=-B for the entrance edge and p1=+B for the exit edge.

    Edge type = DIP
    p1: BY [T]

    Edge type = HDIP
    p1: BX [T]

    Edge type = DIP3
    p1: rotation angle [deg]
    p2: BY0 [T]
    p3: flag 1:in 2:out

    Edge type = QUAD
    p1: gradient [T/m]

    Edge type = SQUA
    p1: gradient [T/m]

    Edge type = SEX
    p1: b2 [T/m2] (cf. C. Wang & L. Teng, MC 207)

    Edge type = BSOL
    p1: BS [T]
    p2: BY [T]
    p3: 0 for entrance face, 1 for exit face

    Edge type = FACE
    This gives vertical focusing from rotated pole faces.
    p1: pole face angle [deg]
    p2: radius of curvature of reference particle [m]
    p3: if not 0 => correct kick by factor 1/(1+delta)
    p4: if not 0 ==> apply horizontal focus with strength = (-vertical strength)
    If a FACE command is used before and after a sector dipole (DIP), you can approximate a rectangular dipole field.
    The DIP, HDIP, QUAD, SQUA, SEX and BSOL edge types use Scott Berg's HRDEND routine to find the change in transverse
    position and transverse momentum due to the fringe field.
    """

    def __init__(
            self,
            edge_type,
            model,
            model_parameters_list,
            name=None,
            metadata=None):
        PseudoRegion.__init__(self, name, metadata)
        self.edge_type = edge_type
        self.model = model
        self.model_parameters = model_parameters


class Cell(RegularRegionContainer):

    """CELL Start of a repeating group of region commands; the data must end with an ENDCELL command.
    The cell loop can enclose any number of commands under REPEAT plus REPEAT and ENDREPEAT commands.
    It has an associated cell field, which is superimposed on the individual region fields. Cell sections cannot
    be nested in other cell sections. (see parameters below)
    """
    begtag = 'CELL'
    endtag = 'ENDCELL'
    num_params = 3
    for001_format = {'line_splits': [1, 1, 1]}

    allowed_enclosed_commands = [
        'SRegion',
        'Aperture',
        'Dens',
        'Disp',
        'Dummy',
        'DVar',
        'Edge',
        'Output',
        'Refp',
        'Ref2',
        'Reset',
        'RKick',
        'Rotate',
        'Tilt',
        'Transport',
        'Repeat']

    command_params = {
        'ncells': {
            'desc': 'Number of times to repeat this command in this cell block',
            'doc': '',
            'type': 'Integer',
            'req': True,
            'pos': 1},
        'flip': {
            'desc': 'if .true. => flip cell field for alternate cells',
            'doc': '',
            'type': 'Logical',
            'req': True,
            'pos': 2},
        'field': {
            'desc': 'Field object',
            'doc': '',
            'type': 'Field',
            'req': True,
            'pos': 3},
    }

    def __init__(self, **kwargs):
        RegularRegion.__init__(self, kwargs)
        Container.__init__(self)

    def __setattr__(self, name, value):
        Container.__setattr__(self, name, value)

    def __str__(self):
        return_str = 'CELL\n' + str(Container.__str__(self)) + 'ENDCELL\n'
        # for command in self.enclosed_commands:
        #    return_str += str(command)
        return return_str

    def __repr__(self):
        return 'Cell\n'


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
        RegularRegion.__init__(self, kwargs)
        Container.__init__(self)

    def __str__(self):
        ret_str = 'SRegion:\n' + 'slen=' + str(self.slen) + '\n' + 'nrreg=' + str(self.nrreg) + '\n' + \
           'zstep=' + str(self.zstep) + '\n' + str(Container.__str__(self))
        return ret_str

    def __repr__(self):
        return 'SRegion:\n ' + 'slen=' + \
            str(self.slen) + '\n' + 'nrreg=' + str(self.nrreg) + \
            '\n' + 'zstep=' + str(self.zstep)

    def __setattr__(self, name, value):
        Container.__setattr__(self, name, value)

    def add_subregion(self, subregion):
        try:
            if self.check_type('SubRegion', subregion):
                if not hasattr(self, 'subregions'):
                    self.subregions = []
                self.subregions.append(subregion)
            else:
                raise ie.InvalidType('SubRegion', subregion.__class__.__name__)
        except ie.InvalidType as e:
            print e

    def add_subregions(self, subregion_list):
        for subregion in subregion_list:
            self.subregions.append(subregion)

    """def gen_for001(self, file):
        if hasattr(self, 'outstep'):
            sreg_copy = copy.deepcopy(self)
            delattr(sreg_copy, 'outstep')
            sreg_copy.slen = self.outstep
            nrep = int(self.slen/self.outstep)
            r = Repeat(nrep=nrep)
            r.add_enclosed_command(sreg_copy)
            r.gen_for001(file)
        else:
            RegularRegionContainer.gen_for001(self, file)"""



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
                 'type': 'Real',
                 'req': True,
                 'pos': 2},

        'rhigh': {'desc': 'Outer radius of this r subregion',
                  'doc': '',
                  'type': 'Real',
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
        RegularRegion.__init__(self, kwargs)

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
        Region.__setattr__(self, name, value)


class ModeledCommandParameter(ICoolObject):

    def __init__(self, kwargs):
        """
        Checks to see whether all required parameters are specified.  If not, raises exception and exits.
        """
        if self.check_command_params_init(kwargs) is False:
            sys.exit(0)
        else:
            if self.check_no_model():
                return
            else:
                setattr(
                    self,
                    self.get_model_descriptor_name(),
                    self.get_model_name_in_dict(kwargs))
                del kwargs[self.get_model_descriptor_name()]
                self.setall(kwargs)

    def __call__(self, kwargs):
        if self.check_command_params_call(kwargs) is False:
            sys.exit(0)
        else:
            if not self.get_model_descriptor_name() in kwargs.keys():
                ICoolObject.__call__(self, kwargs)
            else:
                setattr(
                    self,
                    self.get_model_descriptor_name(),
                    self.get_model_name_in_dict(kwargs))
                del kwargs[self.get_model_descriptor_name()]
                self.setall(kwargs)

    def __setattr__(self, name, value):
        # Check whether the attribute being set is the model
        if name == self.get_model_descriptor_name():
            if self.check_valid_model(value) is False:
                return
            new_model = False
            # Check whether this is a new model (i.e. model was previously
            # defined)
            if hasattr(self, self.get_model_descriptor_name()):
                new_model = True
                # Delete all attributes of the current model
                print 'Resetting model to ', value
                self.reset_model()
            object.__setattr__(self, self.get_model_descriptor_name(), value)
            # If new model, set all attributes of new model to 0.
            if new_model is True:
                self.set_and_init_params_for_model(value)
            return
        try:
            if self.check_command_param(name):
                if self.check_command_param_type(name, value):
                    object.__setattr__(self, name, value)
            else:
                raise ie.SetAttributeError('', self, name)
        except ie.InvalidType as e:
            print e
        except ie.SetAttributeError as e:
            print e

    def __str__(self):
        desc = 'ModeledCommandParameter\n'
        for key in self.get_model_dict(
            getattr(
                self,
                self.get_model_descriptor_name())):
            desc = desc + key + ': ' + str(getattr(self, key)) + '\n'
        return desc

    def set_keyword_args_model_specified(self, kwargs):
        setattr(
            self,
            self.get_model_descriptor_name(),
            kwargs[
                self.get_model_descriptor_name()])
        for key in kwargs:
            if not key == self.get_model_descriptor_name():
                setattr(self, key, kwargs[key])

    def set_keyword_args_model_not_specified(self, kwargs):
        for key in kwargs:
            object.__setattr__(self, key, kwargs[key])

    def reset_model(self):
        for key in self.get_model_parms_dict():
            if hasattr(self, key):
                delattr(self, key)

    def set_and_init_params_for_model(self, model):
        for key in self.get_model_dict(model):
            if key is not self.get_model_descriptor_name():
                setattr(self, key, 0)

    def check_command_params_init(self, command_params):
        """
        Checks if ALL keywords for a model are specified.  If not, raises InputArgumentsError.
        If model is not specified, raises ModelNotSpecifiedError.
        Initialization of a model (e.g., Accel, SOL, etc. requires all keywords specified)
        """
        if self.check_no_model():
            return True
        if not self.check_model_specified(command_params):
            return False
        else:
            if not self.check_valid_model(
                    self.get_model_name_in_dict(command_params)):
                return False
            else:
                command_params_dict = self.get_command_params_for_specified_input_model(
                    command_params)
                if not self.check_command_params_valid(command_params, command_params_dict) \
                    or not self.check_all_required_command_params_specified(command_params, command_params_dict) \
                        or not self.check_command_params_type(command_params, command_params_dict):
                            return False
                else:
                    return True

    def check_command_params_call(self, command_params):
        """
        Checks to see whether new model specified in call.
        If so, checks that the parameters specified correspond to that model and raises an exception if they dont.
        Does NOT require all parameters specified for new model.  Unspecified parameters are set to 0.
        If model is not specified, checks whether the parameters specified correspond to the current model and
        raises an exception otherwise.
        """
        if not self.get_model_descriptor_name() in command_params.keys():
            command_params_dict = self.get_model_parms_dict()
            if not self.check_command_params_valid(command_params, command_params_dict) \
                or not self.check_command_params_type(command_params, command_params_dict):
                    return False
            else:
                return True
        else:
            return self.check_command_params_init(command_params)

    def check_valid_model(self, model):
        """
        Checks whether model specified is valid.
        If model is not valid, raises an exception and returns False.  Otherwise returns True.
        """
        try:
            if not str(model) in self.get_model_names():
                raise ie.InvalidModel(str(model), self.get_model_names())
        except ie.InvalidModel as e:
            print e
            return False
        return True

    def check_partial_keywords_for_current_model(self, input_dict):
        """
        Checks whether the keywords specified for a current model correspond to that model.
        """
        actual_dict = self.get_model_dict(
            getattr(
                self,
                self.get_model_descriptor_name()))
        for key in input_dict:
            if key not in actual_dict:
                raise ie.InputArgumentsError(
                    'Input Arguments Error',
                    input_dict,
                    actual_dict)
        return True

    def check_partial_keywords_for_new_model(self, input_dict):
        """
        Checks whether the keywords specified for a new model correspond to that model.
        """
        model = input_dict[self.get_model_descriptor_name()]
        actual_dict = self.get_model_dict(model)
        for key in input_dict:
            if key not in actual_dict:
                raise ie.InputArgumentsError(
                    'Input Arguments Error',
                    input_dict,
                    actual_dict)
        return True

    def check_model_specified(self, input_dict):
        """
        Check whether the user specified a model in specifying parameters to Init or Call.
        if so, returns True.  Otherwise, raises an exception and returns False.
        """
        try:
            if not self.get_model_descriptor_name() in input_dict.keys():
                raise ie.ModelNotSpecified(self.get_model_names())
        except ie.ModelNotSpecified as e:
            print e
            return False
        return True

    def check_no_model(self):
        if self.get_model_descriptor_name() is None:
            return True
        else:
            return False
    # Helper functions
    ##################################################

    def get_model_descriptor(self):
        """Returns the model descriptor dictionary"""
        return self.models['model_descriptor']

    def get_model_descriptor_name(self):
        """
        The model descriptor name is an alias name for the term 'model', which is specified for each descendent class.
        Returns the model descriptor name.
        """
        return self.get_model_descriptor()['name']

    def get_current_model_name(self):
        """Returns the name of the current model"""
        return getattr(self, self.get_model_descriptor_name())

    def get_model_parms_dict(self):
        """
        Returns the parameter dictionary for the current model.
        """
        if self.get_model_descriptor_name() is None:
            return {}
        else:
            return self.get_model_dict(self.get_current_model_name())

    def get_model_dict(self, model):
        """
        Returns the parameter dictionary for model name.
        """
        return self.models[str(model)]['parms']

    def get_num_params(self):
        """
        Returns the number of parameters for model.
        """
        return self.get_model_descriptor()['num_parms']

    def get_icool_model_name(self):
        """Check to see whether there is an alternate icool_model_name from the common name.
        If so return that.  Otherwise, just return the common name."""
        if 'icool_model_name' not in self.models[
                str(self.get_current_model_name())]:
            return self.get_current_model_name()
        else:
            return self.models[str(self.get_current_model_name())][
                'icool_model_name']

    def get_model_names(self):
        """Returns a list of all model names"""
        ret_list = self.models.keys()
        pos = ret_list.index('model_descriptor')
        del ret_list[pos]
        return ret_list

    def get_model_name_in_dict(self, dict):
        """Returns the model name in a provided dictionary if it exists.  Otherwise returns None"""
        if self.get_model_descriptor_name() not in dict:
            return None
        else:
            return dict[self.get_model_descriptor_name()]

    def get_command_params(self):
        return self.get_model_parms_dict()

    def get_command_params_for_specified_input_model(
            self,
            input_command_params):
        specified_model = input_command_params[
            self.get_model_descriptor_name()]
        return self.get_model_dict(specified_model)

    def get_line_splits(self):
        return self.models['model_descriptor']['for001_format']['line_splits']

    ##################################################

    def set_model_parameters(self):
        parms_dict = self.get_model_parms_dict()
        high_pos = 0
        for key in parms_dict:
            if key['pos'] > high_pos:
                high_pos = key['pos']
        self.parms = [0] * high_pos

    def gen_parm(self):
        num_parms = self.get_num_params()
        command_params = self.get_command_params()
        parm = [0] * num_parms
        for key in command_params:
            pos = int(command_params[key]['pos']) - 1
            if key == self.get_model_descriptor_name():
                val = self.get_icool_model_name()
                print 'Using icool name', val
            else:
                val = getattr(self, key)
            parm[pos] = val
        print parm
        return parm

    def gen_for001(self, file):
        if hasattr(self, 'begtag'):
            print 'Writing begtag'
            # file.write('\n')
            file.write(self.get_begtag())
            file.write('\n')
        parm = self.gen_parm()
        splits = self.get_line_splits()
        count = 0
        split_num = 0
        cur_split = splits[split_num]
        for i in parm:
            if count == cur_split:
                file.write('\n')
                count = 0
                split_num = split_num + 1
                cur_split = splits[split_num]
            file.write(str(i))
            file.write(' ')
            count = count + 1
        file.write('\n')
        if hasattr(self, 'endtag'):
            print 'Writing endtag'
            file.write('\n')
            file.write(self.get_endtag())
            file.write('\n')


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
        ModeledCommandParameter.__init__(self, kwargs)

    def __call__(self, **kwargs):
        ModeledCommandParameter.__call__(self, kwargs)

    def __setattr__(self, name, value):
        ModeledCommandParameter.__setattr__(self, name, value)

    def __str__(self):
        return ModeledCommandParameter.__str__(self)


class Distribution(ModeledCommandParameter):

    """
    A Distribution is a:
    (1) bdistyp (I) beam distribution type {1:Gaussian 2:uniform circular segment}
    (2-13) 12 Parameters for bdistyp
    """

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
        ModeledCommandParameter.__init__(self, kwargs)

    def __call__(self, **kwargs):
        ModeledCommandParameter.__call__(self, kwargs)

    def __setattr__(self, name, value):
        ModeledCommandParameter.__setattr__(self, name, value)

    def __str__(self):
        return ModeledCommandParameter.__str__(self)


class Correlation(ModeledCommandParameter):

    """
    A Correlation is a:
    (1) CORRTYP (I) correlation type
    (2) CORR1(i) (R) correlation parameter 1
    (3) CORR2(i) (R) correlation parameter 2
    (4) CORR3(i) (R) correlation parameter 3
    """
    models = {
        'model_descriptor': {
            'desc': 'Correlation type',
            'name': 'corrtyp',
            'num_parms': 4,
            'for001_format': {
                'line_splits': [4]}
            },
        'ang_mom': {
            'desc': 'Angular momentum appropriate for constant solenoid field',
            'doc': '',
            'icool_model_name': 1,
            'parms': {
                        'corrtyp': {
                            'pos': 1, 'type': 'String', 'doc': ''},
                        'sol_field': {
                            'pos': 2, 'type': 'Real', 'doc': ''}}},
        'palmer': {
            'desc': 'Palmer amplitude correlation',
            'doc': '', 'icool_model_name': 2,
            'parms': {
                        'corrtyp': {
                            'pos': 1, 'type': 'String', 'doc': ''},
                        'strength': {
                            'pos': 2, 'type': 'Real', 'doc': ''},
                        'beta_eff': {
                            'pos': 3, 'type': 'Real', 'doc': ''}}},
        'rf_bucket_ellipse': {
            'desc': 'Rf bucket, small amplitude ellipse',
            'doc': '', 'icool_model_name': 3,
            'parms': {
                        'corrtyp': {
                            'pos': 1, 'type': 'String', 'doc': ''},
                        'e_peak': {
                            'pos': 2, 'type': 'Real', 'doc': ''},
                        'phase': {
                            'pos': 3, 'type': 'Real', 'doc': ''},
                        'freq': {
                            'pos': 4, 'type': 'Real', 'doc': ''}}},
        'rf_bucket_small_separatrix': {
            'desc': 'Rf bucket, small amplitude separatrix',
            'doc': '', 'icool_model_name': 4,
            'parms': {
                        'corrtyp': {
                            'pos': 1, 'type': 'String', 'doc': ''},
                            'e_peak': {
                                'pos': 2, 'type': 'Real', 'doc': ''},
                            'phase': {
                                'pos': 3, 'type': 'Real', 'doc': ''},
                            'freq': {
                                'pos': 4, 'type': 'Real', 'doc': ''}}},
        'rf_bucket_large_separatrix': {
            'desc': 'Rf bucket, small amplitude separatrix',
            'doc': '', 'icool_model_name': 5,
            'parms': {
                        'corrtyp': {
                            'pos': 1, 'type': 'Real', 'doc': ''},
                        'e_peak': {
                            'pos': 2, 'type': 'Real', 'doc': ''},
                        'phase': {
                            'pos': 3, 'type': 'Real', 'doc': ''},
                        'freq': {
                            'pos': 4, 'type': 'Real', 'doc': ''}}},
        'twiss_px': {
            'desc': 'Twiss parameters in x Px',
            'doc': '',
            'icool_model_name': 6,
            'parms': {
                        'corrtyp': {
                            'pos': 1, 'type': 'String', 'doc': ''},
                        'alpha': {
                            'pos': 2, 'type': 'Real', 'doc': ''},
                        'beta': {
                            'pos': 3, 'type': 'Real', 'doc': ''},
                        'epsilon': {
                            'pos': 4, 'type': 'Real', 'doc': ''}}},
        'twiss_py': {
            'desc': 'Twiss parameters in x Px',
            'doc': 'The spread in y and Py in the beam definition are ignored. '
                   'For Gaussian distributions epsilon is the rms geometrical '
                   'emittance. For uniform distributions it specifies the limiting ellipse.',
            'icool_model_name': 7,
            'parms': {
                        'corrtyp': {
                            'pos': 1, 'type': 'String', 'doc': ''},
                        'alpha': {
                            'pos': 2, 'type': 'Real', 'doc': 'Twiss alpha parameter [m]'},
                        'beta': {
                            'pos': 3, 'type': 'Real', 'doc': 'Twiss beta parameter [m]'},
                        'epsilon': {
                            'pos': 4, 'type': 'Real', 'doc': 'Twiss epsilon parameter [m]'}}},
        'equal_sol': {
            'desc': 'Equal time in solenoid.', 'doc': 'Set up with pz and σPz such that βz > βo. '
                    'Set up initial pt = 0. This correlation determines the pt '
                    'for a given pz that gives all the initial particles the same βo. '
                    'If parameter 3 is 0, the azimuthal angle is chosen randomly.',
            'icool_model_name': 9,
            'parms': {
                        'corrtyp': {
                            'pos': 1, 'type': 'String', 'doc': ''},
                        'axial_beta': {
                            'pos': 2, 'type': 'Real', 'doc': 'desired axial beta (=v/c) value βo'},
                        'az_ang_mom': {
                            'pos': 3, 'type': 'Real', 'doc': 'azimuthal angle of transverse momentum [deg]'}}},
        'balbekov': {
            'desc': 'Balbekov version of amplitude-energy.',
            'doc': '',
            'icool_model_name': 10,
            'parms': {
                        'corrtyp': {
                            'pos': 1, 'type': 'String', 'doc': ''},
                        'eref': {
                            'pos': 2, 'type': 'Real', 'doc': 'Eref [GeV]'},
                        'babs': {
                            'pos': 3, 'type': 'Real', 'doc': 'Babs [ T ]'},
                        'sigma_e:': {
                            'pos': 4, 'type': 'Real', 'doc': 'σE [GeV]'}}},
        'dispersion': {
            'desc': 'Dispersion', 'doc': '',
            'icool_model_name': 11,
            'parms': {
                        'corrtyp': {
                            'pos': 1, 'type': 'String', 'doc': ''},
                        'value': {
                            'pos': 2, 'type': 'Real', 'doc': '[m or rad]'},
                        'pref': {
                            'pos': 3, 'type': 'Real', 'doc': '[GeV/c]'},
                        'type': {
                            'pos': 4, 'type': 'Real', 'doc': 'Type flag.  x, y, x_prime, y_prime'}}}}
    
    def __init__(self, **kwargs):
        ModeledCommandParameter.__init__(self, kwargs)

    def __call__(self, **kwargs):
        ModeledCommandParameter.__call__(self, kwargs)

    def __setattr__(self, name, value):
        ModeledCommandParameter.__setattr__(self, name, value)

    def __str__(self):
        return self.corrtyp + ':' + 'Correlation:' + \
            ModeledCommandParameter.__str__(self)


class BeamType(Container):
    """
    A BeamType is a:
    (1) PARTNUM (I) particle number
    (2) BMTYPE (I) beam type {magnitude = mass code; sign = charge}
        1: e
        2: μ
        3: π
        4: K
        5: p
        6: d
        7: He3
        8: Li7
    (3) FRACBT (R) fraction of beam of this type {0-1} The sum of all fracbt(i) should =1.0
    (4) Distribution
    (5) NBCORR # of beam correlations {0-10}
    (6) From 0-10 enclosed Correlation objects as specified by NBCORR (5)

    """
    allowed_enclosed_commands = ['Correlation']

    command_params = {
        'partnum': {
            'desc': 'Particle number',
            'doc': '',
            'type': 'Integer',
            'req': True,
            'default': None},
        'bmtype': {
            'desc': 'beam type {magnitude = mass code; sign = charge}: 1: e, 2: μ, 3: π, 4: K, 5: p. '
            '6: d, 7: He3, 8: Li7',
            'doc': '',
            'out_dict': {
                'e': 1,
                'mu': 2,
                'pi': 3,
                'k': 4,
                'p': 5,
                'd': 6,
                'he3': 7,
                'li7': 8},
            'type': 'Integer',
            'req': True,
            'default': None},
        'fractbt': {
            'desc': 'Fraction of beam of this type {0-1} The sum of all fracbt(i) should =1.0',
                    'doc': '',
                    'type': 'Real',
                    'req': True,
                    'default': None},
        'distribution': {
            'desc': 'Beam distribution object',
            'doc': '',
            'type': 'Distribution',
            'req': True,
            'default': None},
        'nbcorr': {
            'desc': '# of beam correlations {0-10}',
            'doc': '',
            'type': 'Integer',
            'req': True,
            'default': 0,
            'min': 0,
            'max': 10}}

    def __init__(self, **kwargs):
        if self.check_command_params_init(kwargs) is False:
            sys.exit(0)
        ICoolObject.__init__(self, kwargs)
        Container.__init__(self)

    def __setattr__(self, name, value):
        Container.__setattr__(self, name, value)

    def __str__(self):
        return 'BeamType: \n'

    def __repr__(self):
        return '[BeamType: ]'

    def gen_for001(self, file):
        file.write(str(self.partnum))
        file.write(' ')
        file.write(str(self.bmtype))
        file.write(' ')
        file.write(str(self.fractbt))
        file.write('\n')
        self.distribution.gen_for001(file)
        file.write('\n')
        file.write(str(self.nbcorr))
        file.write('\n')
        for c in self.enclosed_commands:
            c.gen_for001(file)


class Field(ModeledCommandParameter):

    """
    A Field is a:
    FTAG - A tag identifying the field.  Valid FTAGS are:
    NONE, ACCEL, BLOCK, BROD, BSOL, COIL, DIP, EFLD, FOFO, HDIP, HELI(
        X), HORN, KICK, QUAD,
    ROD, SEX, SHEE(T), SOL, SQUA, STUS, WIG

    FPARM - 15 parameters describing the field.  The first parameter is the model.
    """

    def __init__(self, ftag, kwargs):
        ModeledCommandParameter.__init__(self, kwargs)
        self.ftag = ftag

    def __call__(self, kwargs):
        ModeledCommandParameter.__call__(self, kwargs)

    def __setattr__(self, name, value):
        if name == 'fparm':
            object.__setattr__(self, name, value)
        else:
            ModeledCommandParameter.__setattr__(self, name, value)

    def __str__(self):
        return self.ftag + ':' + 'Field:' + \
            ModeledCommandParameter.__str__(self)

    def gen_fparm(self):
        self.fparm = [0] * 10
        cur_model = self.get_model_dict(self.model)
        for key in cur_model:
            pos = int(cur_model[key]['pos']) - 1
            if key == self.get_model_descriptor_name():
                val = self.get_icool_model_name()
            else:
                val = getattr(self, key)
            self.fparm[pos] = val
        print self.fparm


class Material(ModeledCommandParameter):

    """
    A Material is a:
    (1) MTAG (A) material composition tag
    (2) MGEOM (A) material geometry tag
    (3-12) GPARM (R) 10 parameters that describe the geometry of the material

    Enter MTAG in upper case.
    Valid MTAG'S are:

    VAC vacuum (i.e., no material)
    GH gaseous hydrogen
    GHE gaseous helium
    LH liquid hydrogen
    LHE liquid helium
    LI BE B C AL TI FE CU W HG PB (elements)
    LIH lithium hydride
    CH2 polyethylene
    SS stainless steel (alloy 304)

    Valid MGEOM's are:

    NONE use for vacuum
    10*0.

    CBLOCK cylindrical block
    10*0.
    ...

    """
    materials = {
        'VAC': {'desc': 'Vacuum (no material)', 'icool_material_name': ''},
        'GH': {'desc': 'Gaseous hydrogen'},
        'GHE': {'desc': 'Gaseous helium'},
        'LH': {'desc': 'Liquid hydrogen'},
        'LHE': {'desc': 'Liquid helium'},
        'LI': {'desc': 'Lithium'},
        'BE': {'desc': 'Berylliyum'},
        'B': {'desc': 'Boron'},
        'C': {'desc': 'Carbon'},
        'AL': {'desc': 'Aluminum'},
        'TI': {'desc': 'Titanium'},
        'FE': {'desc': 'Iron'},
        'CU': {'desc': 'Copper'},
        'W': {'desc': 'Tungsten'},
        'HG': {'desc:': 'Mercury'},
        'PB': {'desc:': 'Lead'}
    }

    models = {
        'model_descriptor': {
            'desc': 'Geometry',
            'name': 'geom',
            'num_parms': 12,
            'for001_format': {
                'line_splits': [1, 1, 10]}},
        'VAC': {
            'desc': 'Vacuum',
            'doc': 'Vacuum region.  Specify vacuum for mtag.  Geom will be set to NONE.',
            'parms': {
                'mtag': {
                           'pos': 1, 'type': 'String', 'doc': ''}}},
        'CBLOCK': {
            'desc': 'Cylindrical block',
            'doc': 'Cylindrical block',
            'parms': {
                'mtag': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'geom': {
                    'pos': 2, 'type': 'String', 'doc': ''}}},
        'ASPW': {
            'desc': 'Azimuthally Symmetric Polynomial Wedge absorber region', 'doc': 'Edge shape given by '
                    'r(dz) = a0 + a1*dz + a2*dz^2 + a3*dz^3 in the 1st quadrant and '
                    'where dz is measured from the wedge center. '
                    '1 z position of wedge center in region [m] '
                    '2 z offset from wedge center to edge of absorber [m] '
                    '3 a0 [m] '
                    '4 a1 '
                    '5 a2 [m^(-1)] '
                    '6 a3 [m^(-2)]',
            'parms': {
                'mtag': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'geom': {
                    'pos': 2, 'type': 'String', 'doc': ''},
                'zpos': {
                    'pos': 3, 'type': 'Real', 'doc': ''},
                'zoff': {
                    'pos': 4, 'type': 'Real', 'doc': ''},
                'a0': {
                    'pos': 5, 'type': 'Real', 'doc': ''},
                'a1': {
                    'pos': 6, 'type': 'Real', 'doc': ''},
                'a2': {
                    'pos': 7, 'type': 'Real', 'doc': ''},
                'a3': {
                    'pos': 8, 'type': 'Real', 'doc': ''}}},
        'ASRW': {
            'desc': 'Azimuthally Symmetric Polynomial Wedge absorber region',
            'doc':  'Edge shape given by '
                    'r(dz) = a0 + a1*dz + a2*dz^2 + a3*dz^3 in the 1st quadrant and '
                    'where dz is measured from the wedge center. '
                    '1 z position of wedge center in region [m] '
                    '2 z offset from wedge center to edge of absorber [m] '
                    '3 a0 [m] '
                    '4 a1 '
                    '5 a2 [m^(-1)] '
                    '6 a3 [m^(-2)]',
            'parms': {
                'mtag': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'geom': {
                    'pos': 2, 'type': 'String', 'doc': ''},
                'zpos': {
                    'pos': 3, 'type': 'Real', 'doc': ''},
                'zoff': {
                    'pos': 4, 'type': 'Real', 'doc': ''},
                'a0': {
                    'pos': 5, 'type': 'Real', 'doc': ''},
                'a1': {
                    'pos': 6, 'type': 'Real', 'doc': ''},
                'a2': {
                    'pos': 7, 'type': 'Real', 'doc': ''},
                'a3': {
                    'pos': 8, 'type': 'Real', 'doc': ''}}},
        'HWIN': {
            'desc': 'Hemispherical absorber end region',
            'doc': '1 end flag {-1: entrance, +1: exit} '
                   '2 inner radius of window[m] '
                   '3 window thickness [m] '
                   '4 axial offset of center of spherical window from start of end region [m]',
            'parms': {
                'mtag': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'geom': {
                    'pos': 2, 'type': 'String', 'doc': ''},
                'end_flag': {
                    'pos': 3, 'type': 'Real', 'doc': '1 end flag {-1: entrance, +1: exit} '},
                'in_rad': {
                    'pos': 4, 'type': 'Real', 'doc': 'Inner radius of window'},
                'thick': {
                    'pos': 5, 'type': 'Real', 'doc': 'Thickness of window'},
                'offset': {
                    'pos': 6, 'type': 'Real', 'doc': 'Axial offset of center of spherical '
                                                     'window from start of end region [m]'}}},
        'NIA': {
            'desc': 'Non-isosceles absorber',
            'doc': '1 zV distance of wedge “center” from start of region [m] '
                   '2 z0 distance from center to left edge [m] '
                   '3 z1 distance from center to right edge [m] '
                   '4 θ0 polar angle from vertex of left edge [deg] '
                   '5 φ0 azimuthal angle of left face [deg] '
                   '6 θ1 polar angle from vertex of right edge [deg] '
                   '7 φ1 azimuthal angle of right face [deg]',
            'parms': {
                'mtag': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'geom': {
                    'pos': 2, 'type': 'String', 'doc': ''},
                'zv': {
                    'pos': 3, 'type': 'Real', 'doc': 'Distance of wedge “center” from start of region [m]'},
                'z0': {
                    'pos': 4, 'type': 'Real', 'doc': 'Distance from center to left edge [m] '},
                'z1': {
                    'pos': 5, 'type': 'Real', 'doc': 'Distance from center to right edge [m]}'},
                'θ0': {
                    'pos': 6, 'type': 'Real', 'doc': 'Polar angle from vertex of left edge [deg]'},
                'φ0': {
                    'pos': 7, 'type': 'Real', 'doc': 'Azimuthal angle of left face [deg]'},
                'θ1': {
                    'pos': 8, 'type': 'Real', 'doc': 'Polar angle from vertex of right edge [deg] '},
                'φ1': {
                    'pos': 9, 'type': 'Real', 'doc': 'Azimuthal angle of right face [deg]'}}},
        'PWEDGE': {
            'desc': 'Asymmetric polynomial wedge absorber region',
            'doc': 'Imagine the wedge lying with its narrow end along the x axis. The wedge is symmetric about the '
                   'x-y plane. The edge shape is given by dz(x) = a0 + a1*x + a2*x^2 + a3*x^3 '
                   'where dz is measured from the x axis.',
            'parms': {
                'mtag': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'geom': {
                    'pos': 2, 'type': 'String', 'doc': ''},
                'init_vertex': {
                    'pos': 3, 'type': 'Real', 'doc': 'Initial position of the vertex along the x axis [m]'},
                'z_wedge_vertex': {
                    'pos': 4, 'type': 'Real', 'doc': 'z position of wedge vertex [m] '},
                'az': {
                    'pos': 5, 'type': 'Real', 'doc': 'Azimuthal angle of vector pointing to vertex in plane of wedge w.r.t. +ve x-axis [deg]'},
                'width': {
                    'pos': 6, 'type': 'Real', 'doc': 'Total width of wedge in dispersion direction [m]'},
                'height': {
                    'pos': 7, 'type': 'Real', 'doc': 'Total height of wedge in non-dispersion direction [m]'},
                'a0': {
                    'pos': 8, 'type': 'Real', 'doc': 'Polar angle from vertex of right edge [deg] '},
                'a1': {
                    'pos': 9, 'type': 'Real', 'doc': 'Azimuthal angle of right face [deg]'},
                'a2': {
                    'pos': 10, 'type': 'Real', 'doc': 'Polar angle from vertex of right edge [deg] '},
                'a3': {
                    'pos': 11, 'type': 'Real', 'doc': 'Azimuthal angle of right face [deg]'}}},
        'RING': {
            'desc': 'Annular ring of material',
            'doc': 'This is functionally equivalent to defining a region with two radial subregions, the first of '
                   'which has vacuum as the material type. However, the boundary crossing algorithm used for RING is '
                   'more sophisticated and should give more accurate simulations.',
            'parms': {
                'mtag': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'geom': {
                    'pos': 2, 'type': 'String', 'doc': ''},
                'inner': {
                    'pos': 3, 'type': 'Real', 'doc': 'Inner radius (R) [m]'},
                'outer': {
                    'pos': 4, 'type': 'Real', 'doc': 'Outer radius (R) [m]'}}},
        'WEDGE': {
            'desc': 'Asymmetric wedge absorber region',
            'doc': 'We begin with an isosceles triangle, sitting on its base, vertex at the top. '
                   'The base-to-vertex distance is W. The full opening angle at the vertex is A. Using '
                   'two of these triangles as sides, we construct a prism-shaped wedge. The distance from '
                   'one triangular side to the other is H. The shape and size of the wedge are now established. '
                   'We define the vertex line of the wedge to be the line connecting the vertices of its two '
                   'triangular sides.  Next, we place the wedge in the right-handed ICOOL coordinate system. '
                   'The beam travels in the +Z direction. Looking downstream along the beamline (+Z into the page), '
                   '+X is horizontal and to the left, and +Y is up.  Assume the initial position of the wedge is as '
                   'follows: The vertex line of the wedge is vertical and lies along the Y axis, extending from Y = -H/2 '
                   'to Y = +H/2. The wedge extends to the right in the direction of -X, such that it is symmetric about '
                   "the XY plane. (Note that it is also symmetric about the XZ plane.) From the beam's point of view, "
                   'particles passing on the +X side of the Y axis will not encounter the wedge, while particles passing '
                   'on the -X side of the Y axis see a rectangle of height H and width W, centered in the Y direction, with '
                   'Z thickness proportional to -X.  '
                   'By setting parameter U to a non-zero value, the user may specify that the wedge is to be '
                   'translated in the X direction. If U>0, the wedge is moved (without rotation) in the +X direction. '
                   'For example, if U = W/2, then the wedge is centered in the X direction; its vertex is at X = W/2 '
                   'and its base is at X = -W/2. Note that the wedge is still symmetric about both the XY plane and '
                   'the XZ plane. '
                   'Next, the wedge may be rotated about the Z axis by angle PHI. Looking downstream in the beam '
                   'direction, positive rotations are clockwise and negative rotations are counter-clockwise. For '
                   'example, setting PHI to 90 degrees rotates the wedge about the Z axis so that its vertex line is '
                   'parallel to the X axis and on top, while its base is parallel to the XZ plane and at the bottom. In '
                   'general this rotation breaks the symmetry about the XZ plane, but the symmetry about the XY '
                   'plane is maintained. '
                   'Finally, the wedge is translated in the Z direction by a distance Zv, so that its XY symmetry plane '
                   'lies a distance Zv downstream of the start of the region. Usually Zv should be at least large '
                   'enough so that the entire volume of the wedge lies within its region, i.e. Zv .ge. W tan (A/2), the '
                   'maximum Z half-thickness of the wedge. As well, the region usually should be long enough to '
                   'contain the entire volume of the wedge, i.e. RegionLength .ge. Zv + W tan (A/2). Wedges that do '
                   'lie completely within their region retain their symmetry about the XY plane Z=Zv.  '
                   'If portions of a wedge lie outside their region in Z, then the volume of the wedge lying outside '
                   'the region is ignored when propagating particles through the wedge. Such a wedge will grow in '
                   'thickness until it reaches the region boundary, but will not extend beyond it. In such cases, '
                   'wedges may lose their symmetry about the XY plane Z=Zv.'
                   'Wedges may be defined such that they extend outside the radial boundaries of the radial '
                   'subregion within which they are defined. However, any portion of the wedge volume lying inside the inner '
                   'radial boundary or outside the outer radial boundary is ignored when propagating particles through '
                   'the wedge. For example, if the user intends that an entire radial subregion of circular cross-section be '
                   'filled with a wedge, then it is clear that the corners of the wedge must extend outside the radial region, '
                   "but particles passing outside the wedge's radial subregion will not see the wedge at all.  "
                   'In short, we may say that although it is permitted (and sometimes essential) to define a wedge to '
                   'be larger than its subregion, for the purposes of particle propagation the wedge is always trimmed at the '
                   "region's Z boundaries and the subregion's radial boundaries. Any volume within the region and subregion "
                   'that is not occupied by the material specified for the wedge is assumed to be vacuum.'
                   '------------------------------------------------------------------------------------------------------------'
                   'Example 1: Within a region 0.4 meters long in Z, within a radial subregion extending from the Z axis out '
                   'to a radius of 0.3 meters, a wedge is to fill the X<0 (right) half of the 0.3 meter aperture of the '
                   'subregion, and increase in Z thickness proportional to -X, such that it is 0.2 meters thick at the '
                   'rightmost point in the subregion (X=-0.3, Y=0).  The wedge is to be 0.2 meters thick at a point 0.3 '
                   'meters from its vertex. The half-thickness is 0.1 meters, the half-opening angle is '
                   'atan (0.1/0.3) = 18.4 degrees, so the full opening angle of the wedge A is 36.8 degrees. The width '
                   '(X extent) of the wedge must be 0.3 meters, and the height (Y extent) of the wedge must be 0.6 meters. '
                   'Two corners of the wedge extend well beyond the subregion, but they will be ignored during particle '
                   'propagation. The wedge does not need to be translated in X (U = 0) nor does it need to be rotated '
                   'about the Z axis (PHI = 0). For convenience we center the wedge (in Z) within its region, '
                   'so Zv = 0.2 meters. Since the maximum half-thickness of the wedge is only 0.1 meters, the wedge '
                   'does not extend beyond (or even up to) the Z boundaries of the region. The volume within the region '
                   'and subregion but outside the wedge is assumed to be vacuum.'
                   '------------------------------------------------------------------------------------------------------------'
                   'Example 2: In the same region and subregion, we need a wedge with the same opening angle, '
                   'but filling the entire aperture of the subregion, thickness gradient in the +Y direction, thickness = '
                   '0 at the lowest point in the subregion (X=0, Y=-0.3).'
                   'The wedge must now have H = W = 0.6 meters so it can fill the entire aperture of the subregion.'
                   'From its initial position, it must first be translated 0.3 meters in the +X direction (U = 0.3) to '
                   "center it in the subregion's aperture, and then (from the perspective of someone looking "
                   'downstream along the beam) rotated counterclockwise 90 degrees (PHI = -90.) so that the Z '
                   'thickness increases proportionally to +Y. Since the wedge has the same opening angle as before '
                   'but has twice the width, its maximum Z thickness is now 0.4 meters, just barely fitting between '
                   'the Z boundaries of the region if Zv = 0.2 meters. All four corners of the wedge now extend '
                   "outside the radial subregion's outer boundary, but they will be ignored during particle "
                   'propagation.” {S.B.}'
                   'The wedge geometry can accept a second MTAG parameter in the SREGION construct. The first material '
                   'refers to the interior of the wedge. The second material, if present, refers to the exterior of the wedge. '
                   'If a second MTAG parameter is not present, vacuum is assumed.',
            'parms': {
                'mtag': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'geom': {
                    'pos': 2, 'type': 'String', 'doc': ''},
                'vert_ang': {
                    'pos': 3, 'type': 'Real', 'doc': 'Full angle at vertex, α (or A) [degrees]the x axis [m]'},
                'vert_init': {
                    'pos': 4, 'type': 'Real', 'doc': 'Initial position of the vertex along the x axis, U [m]'},
                'vert_z': {
                    'pos': 5, 'type': 'Real', 'doc': 'Z position of wedge vertex, Zv [m]'},
                'vert_az': {
                    'pos': 6, 'type': 'Real', 'doc': 'azimuthal angle φ of vector pointing to vertex in plane of wedge w.r.t. +ve x-axis [deg]'},
                'width': {
                    'pos': 7, 'type': 'Real', 'doc': 'Total width of wedge in dispersion direction, w [m]'},
                'height': {
                    'pos': 8, 'type': 'Real', 'doc': 'Total height of wedge in non-dispersion direction, h [m]'}}}}

    def __init__(self, **kwargs):
        ModeledCommandParameter.__init__(self, kwargs)

    def __setattr__(self, name, value):
        if name == 'mparm':
            object.__setattr__(self, name, value)
        else:
            ModeledCommandParameter.__setattr__(self, name, value)

    def __str__(self):
        return 'Material:' + ModeledCommandParameter.__str__(self)

    def gen_mparm(self):
        self.mparm = [0] * 12
        cur_model = self.get_model_dict(self.geom)
        for key in cur_model:
            pos = int(cur_model[key]['pos']) - 1
            val = getattr(self, key)
            self.mparm[pos] = val
        print self.mparm

    def gen(self, file):
        file.write('\n')
        file.write(self.mtag)
        file.write('\n')
        file.write(self.mgeom)
        file.write('\n')
        for s in mparm:
            file.write(s)
            file.write(" ")


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
        Field.__init__(self, 'NONE', kwargs)

    def __call__(self, **kwargs):
        Field.__call__(self, kwargs)

    def __setattr__(self, name, value):
        if name == 'ftag':
            if value == 'NONE':
                object.__setattr__(self, name, value)
            else:
                # Should raise exception here
                print '\n Illegal attempt to set incorrect ftag.\n'
        else:
            Field.__setattr__(self, name, value)

    def __str__(self):
        # return Field.__str__(self)
        return 'NONE'

    def gen_fparm(self):
        Field.gen_fparm(self)


class Accel(Field):

    """ACCE(L) linear accelerator fields
    1 Model
    1: EZ only with no transverse variation
    2: cylindrical TM01p pillbox resonator
    3: traveling wave cavity
    4: approximate fields for symmetric circular-nosed cavity
    5: user-supplied azimuthally-symmetric TM mode (SuperFish) RF field
    6: induction linac model - waveform from user-supplied polynomial coefficients
    7: induction linac model - internally generated waveform
    8: induction linac model - waveform from user-supplied file
    9: sector-shaped pillbox cavity (circular cross section)
    10: variable {frequency, gradient} pillbox cavity
    11: straight pillbox or SuperFish cavity in dipole region
    12: sector-shaped pillbox cavity (rectangular cross section)
    13: open cell standing wave cavity

    The initial phase parameter can be used for any PHASEMODEL and ACCEL models 1-5.

    For model = 1
    2 frequency [MHz]
    3 gradient on-axis at center of gap [MV/m]
    4 phase shift [deg] {0-360}
    5 parameter to approximate a rectangular cavity in cylindrical geometry.
    if set to radius of curvature rho, then E_z is scaled by 1-x/rho, where x is the horizontal
    distance from the reference circle.
    6 (not used)
    7 (not used)
    8 mode
    0 : time-independent
    1: sinusoidal time variation

    For model = 2
    2 frequency f [MHz]
    3 gradient on-axis at center of gap [MV/m]
    4 phase shift [deg] {0-360}.
    5 parameter to approximate a rectangular cavity in cylindrical geometry; if set to radius of
    curvature rho, then the field components are scaled by 1-x/rho, where x is the horizontal
    distance from the reference circle.
    6 x offset of cavity [m]
    7 y offset of cavity [m]
    8 longitudinal mode p {0,1}
    For mode = 0 Rcav = 0.383 * lambda
    For mode = 1 Rcav = 2.405 / {(2pi f)^2 - (pi/SLEN)^2)}^(1/2)

    For model = 3
    2 frequency f [MHz]
    3 gradient on-axis at center of gap [MV/m]
    4 phase shift [deg] {0-360}.
    5 (not used)
    6 (not used)
    7 (not used)
    8 phase velocity of RF wave B_omega. {0<B_omega<1}

    For model = 4
    2 frequency [MHz]
    3 gradient on-axis at center of gap [MV/m]
    4 phase shift [deg] {0-360}.
    5 (not used)
    6 (not used)
    7 (not used)
    8 total length of cavity [m]
    9 total gap [m]
    10 radius of drift tube [m]
    11 radius of nose piece [m]

    For model = 5
    2 frequency[MHz]
    4 phase shift [deg] {0-360}.
    8 file ## of azimuthally symmetric RF input file (see below) {20-99}
    9 field strength normalization factor [MV/m] This multiplies the value in the SuperFish file.
    10 radial cutoff for cavity [m]
    11 axial distance from start of region to centerline of cavity [m]
    12 axial symmetry through center of cavity
    0: symmetric
    1: not symmetric
    ##.DAT has the same format as the Parmela output of
    The contents of the user-supplied file FOR0
    the SuperFish postprocessor SF07.
    1.1 zmin Start of axial grid [cm]
    1.2 zmax End of axial grid [cm]
    1.3 Nz # of z grid points {<251}
    2 frequency [MHz]
    3.1 rmin Start of radial grid [cm]
    3.2 rmax End of radial grid [cm]
    3.3 Nr # of r grid points {<151}
    for ir=1,Nr
    for iz=1,Nz
    4.1 Ez axial electric field [MV/m]
    4.2 Er radial electric field [MV/m]
    4.3 E magnitude of electric field [MV/m]
    4.4 Hphi azimuthal magnetic field [A/m]
    next iz
    next ir
    The grids should extend beyond the region where tracking will occur.

    For model = 6
    2 time offset from start of voltage pulse[s]
    3 accelerator gap [m]
    4 time reset parameter (see below)
    5 V0 term in polynomial expansion of voltage pulse [V ]
    6 V1 term in polynomial expansion of voltage pulse [V / mu_ss]
    7 V2 term in polynomial expansion of voltage pulse [V / mu_s^2]
    8 V3 term in polynomial expansion of voltage pulse [V / mu_s^3]
    9 V4 term in polynomial expansion of voltage pulse [V / mu_s^4]
    10 V5 term in polynomial expansion of voltage pulse[V / mu_s^5]
    11 V6 term in polynomial expansion of voltage pulse[V / mu_s^6]
    12 V7 term in polynomial expansion of voltage pulse[V / mu_s^7]
    13 V8 term in polynomial expansion of voltage pulse[V / mu_s^8]

    This model generates an EZ field across the accelerator gap. The field is time
    dependent, but does not depend on z or r. The radial electric field and azimuthal
    magnetic fields are assumed to be negligible. When the time reset parameter is 1,
    the start time for the voltage pulse is determined from the time the reference particle
    #2 above. Subsequent cells
    entered the cell. The user can adjust this time using parameter
    #4 set to 0 to sample later portions of the same voltage pulse.
    should use parameter
    #4 back to 1.
    A new pulse shape can be started at any time by setting parameter

    For model = 7
    2 number of gaps
    3 starting voltage [GV]
    4 voltage swing [GV]
    5 time offset [s]
    6 target kinetic energy [GeV]
    7 pulse duration [s]
    8 parameter to adjust slope at end of voltage pulse
    9 number of bins in voltage pulse
    10 gap length [m]
    # of output diagnostic file {20-99} (Set this <20 for no diagnostic
    # output.)
    11 file
    12 kill particle flag (Set=1 to eliminate non-useful particles)
    13 restart flag (Set =1 to restart calculation)
    This model, based on a routine by Charles Kim, uses the local E-t phase space to create a voltage
    waveform that attempts to flatten out the kinetic energy along the pulse. The diagnostic file contains
    the following information:
    Region number
    Time bin, n
    t(n)
    V(n)
    EK(n)
    wt1(n) total event weight in this bin
    wt2(n) event weight inside the chosen energy range
    sigEK(n)
    Vstart
    Vend

    For model = 8
    2 time offset from start of voltage pulse[s]
    3 accelerator gap [m]
    4 time reset parameter [s](see below)
    5 file number of waveform input (see format below) {20-99}
    6 polynomial interpolation order, 1=> linear, 2=>quadratic, etc. {1-3}
    7 file # for output diagnostic file (see format below){20-99}
    8 time increment between diagnostic outputs to file [s]
    This model generates an EZ field across the accelerator gap. The field is time
    dependent, but does not depend on z or r. The radial electric field and azimuthal
    magnetic fields are assumed to be negligible. The gap parameter is used to convert
    the voltage profile into an electric field. The field is applied everywhere in the region.
    When the time reset parameter is 1, the start time for the voltage pulse is determined
    from the time the reference particle entered the cell. The user can adjust this time using
    # 2 above. Subsequent cells can use parameter #4 set to 0 to sample later
    # portions of
    parameter
    #4
    the same voltage pulse. A new pulse shape can be started at any time by setting parameter
    back to 1.
    The contents of the waveform input file FOR0##.DAT is
    1) number of points N {1-100}
    This is followed by N pairs
    2) t(i) V(i) [s] [V]
    An output diagnostic file is initialized for an induction linac region where the time reset
    parameter=1 and parameter 7 above is in the range {20-99}. Output occurs when the elapsed
    time from the previous output exceeds the increment given in parameter 8. Output continues for
    subsequent induction linac regions provided parameter 7 remains in the specified range. The
    contents of the file are
    1) column id header
    2) region particle z t Ez

    For model = 9
    2 frequency f[MHz]
    3 gradient on-axis at center of gap [MV/m]
    4 phase shift [deg] {0-360}.

    For model = 10
    2 (not used)
    3 (not used)
    4 phase shift [deg] {0-360}.
    5 number of wavelengths separating the two reference particles
    6 reset parameter (see below)
    7 Total length L of buncher [m]
    8 g0 [MV/m]
    9 g1 [MV/m]
    10 g2 [MV/m]
    11 (not used)
    12 phase model
    0: 0-crossing time set by tREFP
    1: 0-crossing time set by (1/2) * (tREFP + t REF2)
    This model uses a TM010 mode pillbox cavity. It can only be used with REFP and REF2
    defined and phasemodel=2,3,4. The cavity frequency is set using the number of wavelengths
    (parameter 5) and the time difference between the two reference particles. When the reset
    parameter is 1, the starting location of the buncher is determined from the current position
    #6 set to 0 to
    of the reference particle. Subsequent ACCEL commands should use parameter
    sample later portions of the gradient waveform, which is given by
    G = g0 + g1*(z/L) + g2*(z/L)^2
    #6 back to 1.
    A new pulse shape can be started at any time by setting parameter

    For model = 11
    2 frequency f [MHz]
    3 gradient on-axis at center of gap for a pillbox cavity [MV/m]
    4 phase shift [deg] {0-360}.
    5 radial offset of center of cavity from reference trajectory [m]
    6 axial length of cavity [m] If this entered as 0, the program computes the largest pillbox
    cavity that fits in the sector shaped region
    7 cavity type
    0: pillbox
    1: SuperFish
    ## of azimuthally symmetric SuperFish RF input file (see model 5) {20-99}
    8 file
    9 SuperFish field normalization [MV/m] This multiplies the value in the SuperFish file.
    10 SuperFish radial cut off [m]
    11 axial displacement of center of SuperFish cavity from start of the region [m]
    12 SuperFish axial symmetry
    0: symmetric
    1: not symmetric

    For model = 12
    2 frequency f[MHz]
    3 gradient on-axis at center of gap [MV/m]
    4 phase shift [deg] {0-360}.
    5 radial offset of center of cavity from reference trajectory [m]
    6 cavity width [m]
    7 cavity height [m]

    For model = 13
    2 frequency f [MHz]
    3 gradient on-axis at center of gap [MV/m]
    4 phase shift [deg] {0-360}.
    5 flag for hard edge focusing
        0: both entrance and exit focusing
        1: exit focusing only
        2: entrance focusing only
        3: no edge focusing

"""
    begtag = 'ACCEL'
    endtag = ''

    models = {
        'model_descriptor': {
            'desc': 'Name of model parameter descriptor',
            'name': 'model',
            'num_parms': 15,
            'for001_format': {
                'line_splits': [15]}},
        'ez': {
            'desc': 'Ez only with no transverse variation',
            'doc': '',
            'icool_model_name': 1,
            'parms': {
                'model': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'freq': {
                    'pos': 2, 'type': 'Real', 'doc': 'Frequency [MHz]'},
                'grad': {
                    'pos': 3, 'type': 'Real', 'doc': 'Gradient on-axis at center of gap [MV/m]'},
                'phase': {
                    'pos': 4, 'type': 'Real', 'doc': 'Phase shift [deg] {0-360}.'},
                'rect_cyn': {
                    'pos': 5, 'type': 'Real', 'doc': 'Parameter to approximate a rectangular cavity '
                                      'in cylindrical geometry; if set to radius of curvature ρ, then EZ is scaled by '
                                      '1-x/ ρ, where x is the horizontal distance from the reference circle.'},
                'mode': {
                    'pos': 8, 'type': 'Int', 'doc': '0 : Time-independent 1: sinusoidal time variation'}}},
        'cyn_pill': {
            'desc': 'Cylindrical TM01p pillbox',
            'doc': '', 'icool_model_name': 2,
            'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'freq': {
                        'pos': 2, 'type': 'Real', 'doc': ''},
                    'grad': {
                        'pos': 3, 'type': 'Real', 'doc': ''},
                    'phase': {
                        'pos': 4, 'type': 'Real', 'doc': ''},
                    'rect_cyn': {
                        'pos': 5, 'type': 'Real', 'doc': ''},
                    'longitudinal_mode': {
                        'pos': 8, 'type': 'Real', 'doc': ''}}},
        'trav': {
            'desc': 'Traveling wave cavity',
            'doc': '',
            'icool_model_name': 3,
            'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'freq': {
                        'pos': 2, 'type': 'Real', 'doc': ''},
                    'grad': {
                        'pos': 3, 'type': 'Real', 'doc': ''},
                    'phase': {
                        'pos': 4, 'type': 'Real', 'doc': ''},
                    'rect_cyn': {
                        'pos': 5, 'type': 'Real', 'doc': ''},
                    'x_offset': {
                        'pos': 6, 'type': 'Real', 'doc': ''},
                    'y_offset': {
                        'pos': 7, 'type': 'Real', 'doc': ''},
                    'phase_velocity': {
                        'pos': 8, 'type': 'Real', 'doc': ''}}},
        'circ_nose': {
            'desc': 'Approximate fields for symmetric circular-nosed cavity',
            'doc': '',
            'icool_model_name': 4,
            'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'freq': {
                        'pos': 2, 'type': 'Real', 'doc': ''},
                    'grad': {
                        'pos': 3, 'type': 'Real', 'doc': ''},
                    'phase': {
                        'pos': 4, 'type': 'Real', 'doc': ''},
                    'length': {
                        'pos': 8, 'type': 'Real', 'doc': ''},
                    'gap': {
                        'pos': 9, 'type': 'Real', 'doc': ''},
                    'drift_tube_radius': {
                        'pos': 10, 'type': 'Real', 'doc': ''},
                    'nose_radius': {
                        'pos': 11, 'type': 'Real', 'doc': ''}}},
        'az_tm': {
            'desc': 'User-supplied azimuthally-symmetric TM mode (SuperFish)',
            'doc': '', 'icool_model_name': 5,
            'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'freq': {
                        'pos': 2, 'type': 'Real', 'doc': ''},
                    'phase': {
                        'pos': 4, 'type': 'Real', 'doc': ''},
                    'file_no': {
                        'pos': 8, 'type': 'Real', 'doc': ''},
                    'field_strength_norm': {
                        'pos': 9, 'type': 'Real', 'doc': ''},
                    'rad_cut': {
                        'pos': 10, 'type': 'Real', 'doc': ''},
                    'axial_dist': {
                        'pos': 11, 'type': 'Real', 'doc': ''},
                    'daxial_sym': {
                        'pos': 12, 'type': 'Real', 'doc': ''}}},
        'ilpoly': {
            'desc': 'Induction linac model - waveform from user-supplied polynomial coefficients',
            'doc': '', 'icool_model_name': 6,
            'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'time_offset': {
                        'pos': 2, 'type': 'Real', 'doc': ''},
                    'gap': {
                        'pos': 3, 'type': 'Real', 'doc': ''},
                    'time_reset': {
                        'pos': 4, 'type': 'Real', 'doc': ''},
                    'v0': {
                        'pos': 5, 'type': 'Real', 'doc': ''},
                    'v1': {
                        'pos': 6, 'type': 'Real', 'doc': ''},
                    'v2': {
                        'pos': 7, 'type': 'Real', 'doc': ''},
                    'v3': {
                        'pos': 8, 'type': 'Real', 'doc': ''},
                    'v4': {
                        'pos': 9, 'type': 'Real', 'doc': ''},
                    'v5': {
                        'pos': 10, 'type': 'Real', 'doc': ''},
                    'v6': {
                        'pos': 11, 'type': 'Real', 'doc': ''},
                    'v7': {
                        'pos': 12, 'type': 'Real', 'doc': ''},
                    'v8': {
                         'pos': 13, 'type': 'Real', 'doc': ''}}},
        'ilgen': {
            'desc': 'Induction linac model - waveform from internally generated waveform',
            'doc': '',
            'icool_model_name': 7,
            'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'num_gaps': {
                        'pos': 2, 'type': 'Real', 'doc': ''},
                    'start_volt': {
                        'pos': 3, 'type': 'Real', 'doc': ''},
                    'volt_swing': {
                        'pos': 4, 'type': 'Real', 'doc': ''},
                    'time_offset': {
                        'pos': 5, 'type': 'Real', 'doc': ''},
                    'kin': {
                        'pos': 6, 'type': 'Real', 'doc': ''},
                    'pulse_dur': {
                        'pos': 7, 'type': 'Real', 'doc': ''},
                    'slope': {
                        'pos': 8, 'type': 'Real', 'doc': ''},
                    'bins': {
                        'pos': 9, 'type': 'Real', 'doc': ''},
                    'gap_len': {
                        'pos': 10, 'type': 'Real', 'doc': ''},
                    'file_num': {
                        'pos': 11, 'type': 'Real', 'doc': ''},
                    'kill': {
                        'pos': 12, 'type': 'Real', 'doc': ''},
                    'restart': {
                        'pos': 13, 'type': 'Real', 'doc': ''}}},
        'ilfile': {
            'desc': 'Induction linac model - Waveform from user-supplied file',
            'doc': '',
            'icool_model_name': 8,
            'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'time_offset': {
                        'pos': 2, 'type': 'Real', 'doc': ''},
                    'gap': {
                        'pos': 3, 'type': 'Real', 'doc': ''},
                    'time_reset': {
                        'pos': 4, 'type': 'Real', 'doc': ''},
                    'file_num_wav': {
                        'pos': 5, 'type': 'Real', 'doc': ''},
                    'poly_order': {
                        'pos': 6, 'type': 'Real', 'doc': ''},
                    'file_num_out': {
                        'pos': 7, 'type': 'Real', 'doc': ''},
                    'time_inc': {
                        'pos': 8, 'type': 'Real', 'doc': ''}}},
        'sec_pill_circ': {
            'desc': 'Sector-shaped pillbox cavity (circular cross section)',
            'doc': '',
            'icool_model_name': 9,
            'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'freq': {
                        'pos': 2, 'type': 'Real', 'doc': ''},
                    'grad': {
                        'pos': 3, 'type': 'Real', 'doc': ''},
                    'phase': {
                        'pos': 4, 'type': 'Real', 'doc': ''}}},
        'var_pill': {
            'desc': 'Variable {frequency gradient} pillbox cavity',
            'doc': '',
            'icool_model_name': 10,
            'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'phase': {
                        'pos': 2, 'type': 'Real', 'doc': ''},
                    'num_wavelengths': {
                        'pos': 3, 'type': 'Real', 'doc': ''},
                    'reset_parms': {
                        'pos': 4, 'type': 'Real', 'doc': ''},
                    'buncher_len': {
                        'pos': 5, 'type': 'Real', 'doc': ''},
                    'g0': {
                        'pos': 6, 'type': 'Real', 'doc': ''},
                    'g1': {
                        'pos': 7, 'type': 'Real', 'doc': ''},
                    'g2': {
                        'pos': 8, 'type': 'Real', 'doc': ''},
                    'phase_model': {
                        'pos': 9, 'type': 'Real', 'doc': ''}}},
        'straight_pill': {
                'desc': 'Straight pillbox or SuperFish cavity in dipole region',
                'doc': '',
                'icool_model_name': 11,
                'parms': {
                        'model': {
                            'pos': 1, 'type': 'String', 'doc': ''},
                        'freq': {
                            'pos': 2, 'type': 'Real', 'doc': ''},
                        'grad': {
                            'pos': 3, 'type': 'Real', 'doc': ''},
                        'phase': {
                            'pos': 4, 'type': 'Real', 'doc': ''},
                        'radial_offset': {
                            'pos': 5, 'type': 'Real', 'doc': ''},
                        'axial_length': {
                            'pos': 6, 'type': 'Real', 'doc': ''},
                        'cavity_type': {
                            'pos': 7, 'type': 'Real', 'doc': ''},
                        'file_num': {
                            'pos': 8, 'type': 'Real', 'doc': ''},
                        'sf_field_norm': {
                            'pos': 9, 'type': 'Real', 'doc': ''},
                        'sf_rad_cut': {
                            'pos': 10, 'type': 'Real', 'doc': ''},
                        'sf_axial_disp': {
                            'pos': 11, 'type': 'Real', 'doc': ''},
                        'sf_axial_sym': {
                            'pos': 12, 'type': 'Real', 'doc': ''}}},
        'sec_pill_rec': {
                'desc': 'Variable {frequency gradient} pillbox cavity',
                'doc': '', 'icool_model_name': 12,
                'parms': {
                        'model': {
                            'pos': 1, 'type': 'String', 'doc': ''},
                        'freq': {
                            'pos': 2, 'type': 'Real', 'doc': ''},
                        'grad': {
                            'pos': 3, 'type': 'Real', 'doc': ''},
                        'phase': {
                            'pos': 4, 'type': 'Real', 'doc': ''},
                        'rad_offset': {
                            'pos': 5, 'type': 'Real', 'doc': ''},
                        'width': {
                            'pos': 6, 'type': 'Real', 'doc': ''},
                        'height': {
                            'pos': 7, 'type': 'Real', 'doc': ''}}},
        'open_cell_stand': {
                'desc': 'Open cell standing wave cavity',
                'doc': '',
                'icool_model_name': 13,
                'parms': {
                        'model': {
                            'pos': 1, 'type': 'String', 'doc': ''},
                        'freq': {
                            'pos': 2, 'type': 'Real', 'doc': ''},
                        'grad': {
                            'pos': 3, 'type': 'Real', 'doc': ''},
                        'phase': {
                            'pos': 4, 'type': 'Real', 'doc': ''},
                        'focus_flag': {
                            'pos': 5, 'type': 'Real', 'doc': ''}}}}
                            
    def __init__(self, **kwargs):
        Field.__init__(self, 'ACCEL', kwargs)

    def __call__(self, **kwargs):
        Field.__call__(self, kwargs)

    def __setattr__(self, name, value):
        if name == 'ftag':
            if value == 'ACCEL':
                object.__setattr__(self, name, value)
            else:
                # Should raise exception here
                print '\n Illegal attempt to set incorrect ftag.\n'
        else:
            Field.__setattr__(self, name, value)

    def __str__(self):
        return Field.__str__(self)

    def gen_fparm(self):
        Field.gen_fparm(self)

    def gen(self, file):
        Field.gen(self)


class Sol(Field):

    """
    SOL solenoid field
    1 model level
    1: Bz with constant central region + linear ends
    2: dTANH(z) Bz dependence
    3: field from sum of circular current loops
    4: field from annular current sheet
    5: field from thick annular current block
    6: interpolate field from predefined USER r-z grid
    7: tapered radius
    8: hard-edge with adjustable end fields
    9: determine field from file of Fourier coefficients
    10: determine field from file of on-axis field

    For model = 1
    2 field strength [T]
    3 length of central region, CLEN[m] (You can use this to get a tapered field profile)
    4 length of entrance end region, ELEN1 [m] This is the displacement of the
    upstream end of the solenoid from the start of the region.
    5 constant offset for Bz [T]
    Use parameter 5 to get an indefinitely long, constant solenoidal field.
    6 length of exit end region, ELEN2 [m].
    For a symmetric field, set SLEN =CLEN + ELEN1 + ELEN2. Hard-edge field models
    can include the focusing effects of the missing fringe field by using EDGE commands
    before and after the hard-edge field region.

    For model = 2
    2 field strength [T]
    3 length of central region, CLEN[m]
    4 length for end region, ELEN [m] (This is the displacement of the
    upstream end of the solenoid from the start of the region; for a symmetric field, set SLEN =
    CLEN + 2*ELEN.)
    5 order of vector potential expansion {1, 3, 5, 7}
    6 end attenuation length, [m] (Set larger than maximum beam size)
    7 constant offset for Bs [T]

    For model = 3
    2 field strength [T]
    3 length of central region, CLEN[m] (This is the region over which the coils are
    distributed)
    4 length for end region, ELEN[m] (This is the displacement of the
    upstream end of the solenoid from the start of the region; for a symmetric field, set SLEN =
    CLEN + 2*ELEN.)
    5 # of coils loops (equi-spaced over CLEN)
    6 radius of coils [m]
    For a symmetric field with 1 loop, set ELEN=0.5 SLEN.

    For model = 4
    2 field strength [T]
    3 length of sheet [m]
    4 z offset of center of sheet from start of region [m]
    5 radius of sheet [m]

    For model = 5
    2 field strength [T]
    3 length of block [m]
    4 z offset of center of block from start of region [m]
    5 inner radius of block [m]
    6 outer radius of block[m]

    For model = 6
    2 grid ##of user-supplied field {1-4}
    3 interpolation level {1-3}
    1: bi-linear
    2: bi-quadratic polynomial
    3: bi-cubic polynomial
    The required format of the field map is
    title (A80)
    # of z grid points (I) {1-5000}
    # of r grid points (I) {1-100}
    i, j, zi, rj, BZi,j, BRi,j (I, R)

    2 Bc [T] (flat central field strength)
    3 Rc [m] (flat central coil radius)
    4 Lc [m] (central field length)
    5 B1 [T] (starting field strength)
    6 R1 [m] (starting coil radius)
    7 L1 [m] (length of entrance transition region)
    8 B2 [T] (ending field strength)
    9 R2 [m] (ending coil radius)
    10 L2 [m] (length of exit transition region)
    This model applies a geometry cut on particles whose radius exceeds the specified radial taper.

    """

    begtag = 'SOL'
    endtag = ''
    models = {
        'model_descriptor': {
            'desc': 'Name of model parameter descriptor',
            'name': 'model',
            'num_parms': 15,
            'for001_format': {
                'line_splits': [15]}},
        'bz': {
            'desc': 'Bz with constant central region + linear ends',
            'doc': '',
            'icool_model_name': 1,
            'parms': {
                'model': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'strength': {
                    'pos': 2, 'type': 'Real', 'doc': 'Field strength [T] '},
                'clen': {
                    'pos': 3, 'type': 'Real', 'doc': 'Length of central region, CLEN[m] (You can use this to get a tapered field profile)'},
                'elen1': {
                    'pos': 4, 'type': 'Real', 'doc': 'Length of entrance end region, ELEN1 [m].  This is the displacement of the '
                                                     'upstream end of the solenoid from the start of the region'},
                'offset': {
                    'pos': 5, 'type': 'Real', 'doc': 'Use parameter 5 to get an indefinitely long, constant solenoidal field.'},
                'elen2': {
                    'pos': 6, 'type': 'Real', 'doc': 'Length of exit end region, ELEN2 [m]. For a symmetric field, set:'
                                                     'SLEN =CLEN + ELEN1 + ELEN2. '
                                                     'Hard-edge field models can include the focusing effects of the missing fringe '
                                                     'field by using EDGE commands before and after the hard-edge field region'}}},
        'dtanh': {
            'desc': 'dTANH(z) Bz dependence',
            'doc': '',
            'icool_model_name': 2,
            'parms': {
                'model': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'strength': {
                    'pos': 2, 'type': 'Real', 'doc': 'Field strength [T] '},
                'clen': {
                    'pos': 3, 'type': 'Real', 'doc': 'Length of central region, CLEN[m] (You can use this to get a tapered field '
                                                     'profile)'},
                'elen': {
                    'pos': 4, 'type': 'Real', 'doc': 'Length for end region, ELEN [m] (This is the displacement of the upstream end '
                                                     'of the solenoid from the start of the region; for a symmetric field, '
                                                     'set SLEN =CLEN + 2*ELEN.)'},
                'order': {
                    'pos': 5, 'type': 'Real', 'doc': 'Order of vector potential expansion {1, 3, 5, 7}'},
                'att_len': {
                    'pos': 6, 'type': 'Real', 'doc': 'End attenuation length, [m] (Set larger than maximum beam size) '},
                'offset': {
                    'pos': 7, 'type': 'Real', 'doc': 'Constant offset for Bs [T].  For a symmetric field, set'}}},
        'circ': {
            'desc': 'Field from sum of circular current loops',
            'doc': 'For a symmetric field with 1 loop, set ELEN=0.5 SLEN.',
            'icool_model_name': 3,
            'parms': {
                'model': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'strength': {
                    'pos': 2, 'type': 'Real', 'doc': 'Field strength [T] '},
                'clen': {
                    'pos': 3, 'type': 'Real', 'doc': 'Length of central region, CLEN[m]. '
                                                     '(This is the region over which the coils are distributed))'},
                'elen': {
                    'pos': 4, 'type': 'Real', 'doc': 'Length for end region, ELEN [m] (This is the displacement of the upstream end of '
                                                     'the solenoid from the start of the region; for a symmetric field, '
                                                     'set SLEN =CLEN + 2*ELEN.)'},
                'loops': {
                    'pos': 5, 'type': 'Real', 'doc': 'Number of coil loops'},
                'radius': {
                    'pos': 6, 'type': 'Real', 'doc': 'Radius of coils [m]'}}},
        'sheet': {
                'desc': 'Field from annular current sheet',
                'doc': '',
                'icool_model_name': 4,
                'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'strength': {
                        'pos': 2, 'type': 'Real', 'doc': 'Field strength [T] '},
                    'length': {
                        'pos': 3, 'type': 'Real', 'doc': 'Length of sheet [m] '},
                    'z_offset': {
                        'pos': 4, 'type': 'Real', 'doc': 'z offset of center of sheet from start of region [m]'},
                    'radius': {
                        'pos': 5, 'type': 'Real', 'doc': 'Radius of sheet [m]'}}},
        'block': {
                'desc': 'Field from thick annular current block',
                'doc': '',
                'icool_model_name': 5,
                'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'strength': {
                        'pos': 2, 'type': 'Real', 'doc': 'Field strength [T] '},
                    'length': {
                        'pos': 3, 'type': 'Real', 'doc': 'Length of block [m] '},
                    'z_offset': {
                        'pos': 4, 'type': 'Real', 'doc': 'z offset of center of block from start of of region [m]'},
                    'inner': {
                        'pos': 5, 'type': 'Real', 'doc': 'Inner radius of block [m]'},
                    'outer': {
                        'pos': 6, 'type': 'Real', 'doc': 'Outer radius of block [m]'}}},
        'interp': {
                'desc': 'Interpolate field from predefined USER r-z grid',
                'doc': 'The required format of the field map is:\n'
                       'title (A80)\n'
                       '# of z grid points (I) {1-5000}\n'
                       '# of r grid points (I) {1-100}\n'
                       'i, j, zi, rj, BZi,j, BRi,j (I, R)', 'icool_model_name': 6,
                'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'grid': {
                        'pos': 2, 'type': 'Real', 'doc': 'Grid ##of user-supplied field {1-4} '},
                    'level': {
                        'pos': 3, 'type': 'Int', 'doc': 'Interpolation level {1-3}:\n'
                                                        '1: bi-linear\n'
                                                        '2: bi-quadratic polynomial\n'
                                                        '3: bi-cubic polynomial ', 'min': 1, 'max': 3}}},
        'tapered': {
                'desc': 'Tapered radius', 'doc': 'This model applies a geometry cut on particles whose radius '
                                                 'exceeds the specified radial taper.',
                'icool_model_name': 7, 'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'bc': {
                        'pos': 2, 'type': 'Real', 'doc': 'Bc [T] (flat central field strength) '},
                    'rc': {
                        'pos': 3, 'type': 'Real', 'doc': 'Rc [m] (flat central coil radius) '},
                    'lc': {
                        'pos': 4, 'type': 'Real', 'doc': 'Lc [m] (central field length) '},
                    'b1': {
                        'pos': 5, 'type': 'Real', 'doc': 'B1 [T] (starting field strength)'},
                    'r1': {
                        'pos': 6, 'type': 'Real', 'doc': 'R1 [m] (starting coil radius)'},
                    'l1': {
                        'pos': 7, 'type': 'Real', 'doc': 'L1 [m] (length of entrance transition region)'},
                    'b2': {
                        'pos': 8, 'type': 'Real', 'doc': 'B2 [T] (ending field strength)'},
                    'r2': {
                        'pos': 9, 'type': 'Real', 'doc': 'R2 [m] (ending coil radius)'},
                    'l2': {
                        'pos': 10, 'type': 'Real', 'doc': 'L2 [m] (length of exit transition region)'}}},
        'edge': {
                'desc': 'Hard-edge with adjustable end fields',
                'doc': 'The focusing deficit is B2L - ∫B2 ds. The deficit is independent of the focusing effect chosen with parameter 3.',
                'icool_model_name': 8,
                'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'bs': {
                        'pos': 2, 'type': 'Real', 'doc': 'Bc [T] (flat central field strength) '},
                    'foc_flag': {
                        'pos': 3, 'type': 'Integer', 'doc': 'Flag on whether to include end focusing:\n'
                                                            '0: both entrance and exit focusing\n'
                                                            '1: exit focusing only\n'
                                                            '2: entrance focusing only\n'
                                                            '3: no edge focusing ',
                        'min': 0, 'max': 3},
                    'ent_def': {
                        'pos': 4, 'type': 'Real', 'doc': 'Focusing deficit at entrance [T2 m] '},
                    'ex_def': {
                        'pos': 5, 'type': 'Real', 'doc': 'focusing deficit at exit [T2 m]'}}},
        'fourier': {
                'desc': 'Determine field from file of Fourier coefficients',
                'doc': 'The contents of the input file for0JK.dat is\n'
                       '1 title (A80)\n'
                       '2.1 period, λ (R)\n'
                       '2.2 field strength, S (R)\n'
                       '3 maximum Fourier order (I)\n'
                       '(4 repeated for each order)\n'
                       '4.1 order, m (I) {0 – 199}\n'
                       '4.2 cm (R)\n'
                       '4.3 dm (R)\n'
                       'The on-axis field is given by:\n'
                       'f (s) = S Σ ( cm COS(u) + dm SIN(u) )\n'
                       'where u = 2πms / λ.', 'icool_model_name': 9,
                'parms': {
                        'model': {
                            'pos': 1, 'type': 'String', 'doc': ''},
                        'order': {
                            'pos': 2, 'type': 'Integer', 'doc': 'Order of off-axis expansion (I) {1, 3, 5, 7} '},
                        'scale': {
                            'pos': 3, 'type': 'Real', 'doc': '(R) Multiplies field strength '}}},
        'on_axis': {
                'desc': 'Determine field from file of on-axis field',
                'doc': '',
                'icool_model_name': 10,
                'parms': {
                        'model': {
                            'pos': 1, 'type': 'String', 'doc': ''},
                        'file_num': {
                            'pos': 2, 'type': 'Integer', 'doc': 'File number JK for input data (I) File name is for0JK.dat'},
                        'order': {
                            'pos': 3, 'type': 'Integer', 'doc': 'Order of off-axis expansion (I) {1, 3, 5, 7} '},
                        'scale': {
                            'pos': 4, 'type': 'Real', 'doc': '(R) Multiplies field strength '}}}}
                                                                                                                                                            
    def __init__(self, **kwargs):
        Field.__init__(self, 'SOL', kwargs)

    def __call__(self, **kwargs):
        Field.__call__(self, kwargs)

    def __setattr__(self, name, value):
        if name == 'ftag':
            if value == 'SOL':
                object.__setattr__(self, name, value)
            else:
                # Should raise exception here
                print '\n Illegal attempt to set incorrect ftag.\n'
        else:
            Field.__setattr__(self, name, value)

    def __str__(self):
        return Field.__str__(self)

    def gen_fparm(self):
        Field.gen_fparm(self)


class Edge(Field):

    """
    EDGE
    1) edge type (A4) {SOL, DIP, HDIP,DIP3,QUAD,SQUA,SEX, BSOL,FACE}
    2.1) model # (I) {1}
    2.2-5) p1, p2, p3,p4 (R) model-dependent parameters
    Edge type = SOL
    p1: BS [T]
    If the main solenoid field is B, use p1=-B for the entrance edge and p1=+B for the exit edge.
    Edge type = DIP
    p1: BY [T]
    Edge type = HDIP
    p1: BX [T]
    Edge type = DIP3
    p1: rotation angle [deg]
    p2: BY0 [T]
    p3: flag 1:in 2:out
    Edge type = QUAD
    p1: gradient [T/m]
    Edge type = SQUA
    p1: gradient [T/m]
    Edge type = SEX
    p1: b2 [T/m2] (cf. C. Wang & L. Teng, MC 207)
    Edge type = BSOL
    p1: BS [T]
    p2: BY [T]
    p3: 0 for entrance face, 1 for exit face
    Edge type = FACE
    This gives vertical focusing from rotated pole faces.
    p1: pole face angle [deg]
    p2: radius of curvature of reference particle [m]
    p3: if not 0 => correct kick by the factor 1 / (1+δ)
    p4: if not 0 => apply horizontal focus with strength = (-vertical strength)
    If a FACE command is used before and after a sector dipole ( DIP ), you can approximate a rectangular dipole field.
    The DIP, HDIP, QUAD, SQUA, SEX and BSOL edge types use Scott Berg’s HRDEND routine to find the change in
    transverse position and transverse momentum due to the fringe field.
    """

    begtag = 'EDGE'
    endtag = ''

    models = {
        'model_descriptor': {
            'desc': 'Name of model parameter descriptor',
            'name': 'model',
            'num_parms': 6,
            'for001_format': {
                'line_splits': [
                    1,
                    5]}},
        'sol': {
            'desc': 'Solenoid',
                    'doc': '',
                    'icool_model_name': 'SOL',
                    'parms': {
                        'model': {
                            'pos': 1,
                            'type': 'String',
                            'doc': ''},
                        'bs': {
                            'pos': 3,
                            'type': 'Real',
                            'doc': 'p1: BS [T] '
                            'If the main solenoid field is B, use p1=-B for the entrance edge and p1=+B for the '
                            'exit edge. (You can use this to get a tapered field profile)'}}},
    }

    def __init__(self, **kwargs):
        Field.__init__(self, 'EDGE', kwargs)

    def __call__(self, **kwargs):
        Field.__call__(self, kwargs)

    def __setattr__(self, name, value):
        if name == 'ftag':
            if value == 'EDGE':
                object.__setattr__(self, name, value)
            else:
                # Should raise exception here
                print '\n Illegal attempt to set incorrect ftag.\n'
        else:
            Field.__setattr__(self, name, value)

    def __str__(self):
        return Field.__str__(self)

    def gen_fparm(self):
        Field.gen_fparm(self)


class Output(PseudoRegion):
    begtag = 'OUTPUT'
    endtag = ''

    num_params = 0
    for001_format = {'line_splits': [0]}

    command_params = {}

    def __init__(self):
        PseudoRegion.__init__(self, {})


class Comment(PseudoRegion):

    def __init__(self, comment):
        PseudoRegion.__init__(self, None)
        self.comment = comment


class ICoolInput(ICoolObject):

    """This is the actual generated ICoolInput from command objects
    Command objects include:
    Title, Cont, Bmt, Ints, Nhs, Nsc, Nzh, Nrh, Nem, Ncv and region command objects.
    Region command objects are the superclass of all region command objects and are
    subclassed into RegularRegion and PsuedoRegion command objects.

    RegularRegion command objects include: Section, Repeat, Cell and SRegion.
    Section, Begs, Repeat and Cell will typically contain other allowed region command objects
    such as SRegions as permitted by ICool.

    PseudoRegion command objects include:
        Aperture, Cutv, Denp, Dens, Disp, Dummy, Dvar, Edge, Grid, Output, Refp, Ref2, Reset, Rkick,
        Rotate, Taper, Tilt, Transport, Background, Bfield, ! and &

    title is a problem title object.
    cont is a control variables object.
    bmt is a beam generation variables object.
    ints is a physics interactions control variables object.
    nhs is a histogram defintion variables object.
    nsc is a scatterplot definition variables object.
    nzh is a z-history defintion variables object.
    nrh is a r-history defintion variables object.
    nem is an emittance plane definition variables object.
    ncv is a covariance plane definition variables object.
    sec is a region definition variables object, which contains all region definitions.
    """

    command_params = {
        'title': {'desc': 'Title of ICOOL simulation',
                  'doc': '',
                  'type': 'Title',
                  'req': True,
                  'default': None},

        'cont': {'desc': 'ICOOL control variables',
                 'doc': '',
                 'type': 'Cont',
                 'req': True,
                 'default': None},

        'bmt': {'desc': 'ICOOL beam generation variables',
                'doc': '',
                'type': 'Bmt',
                'req': True,
                'default': None},

        'ints': {'desc': 'ICOOL interaction control variables',
                 'doc': '',
                 'type': 'Ints',
                 'req': True,
                 'default': None},

        'nhs': {'desc': 'ICOOL histogram definition variables',
                'doc': '',
                'type': 'Nhs',
                'req': False,
                'default': Nhs()},

        'nsc': {'desc': 'ICOOL scatterplot defintion variables',
                'doc': '',
                'type': 'Nsc',
                       'req': False,
                       'default': Nsc()},

        'nzh': {'desc': 'ICOOL z history definition variables',
                'doc': '',
                'type': 'Nzh',
                'req': False,
                'default': Nzh()},

        'nrh': {'desc': 'ICOOL r history definition variables',
                'doc': '',
                'type': 'Nrh',
                'req': False,
                'default': Nrh()},

        'nem': {'desc': 'ICOOL emittance plane definition variables',
                'doc': '',
                'type': 'Nem',
                       'req': False,
                       'default': Nem()},

        'ncv': {'desc': 'ICOOL covariance plane definition variables',
                'doc': '',
                'type': 'Ncv',
                       'req': False,
                       'default': Ncv()},

        'section': {'desc': 'ICOOL cooling section region definition ',
                    'doc': '',
                    'type': 'Section',
                    'req': True,
                    'default': None}}

    def __init__(self, **kwargs):
        ICoolObject.__init__(self, kwargs)
        ICoolObject.setdefault(self, kwargs)

    def __call__(self, kwargs):
        ICoolObject.__call__(self, kwargs)

    def __str__(self):
        return ICoolObject.__str__(self, 'CONT')

    def add_title(self, title):
        self.title = title

    def add_cont(self, cont):
        self.cont = cont

    def add_sec(self, sec):
        self.sec = sec

    def gen(self, file):
        if self.title is not None:
            self.title.gen_for001(file)
        if self.cont is not None:
            self.cont.gen_for001(file)
        if self.bmt is not None:
            self.bmt.gen_for001(file)
        if self.ints is not None:
            self.ints.gen_for001(file)
        if self.nhs is not None:
            self.nhs.gen_for001(file)
        if self.nsc is not None:
            self.nsc.gen_for001(file)
        if self.nzh is not None:
            self.nzh.gen_for001(file)
        if self.nrh is not None:
            self.nrh.gen_for001(file)
        if self.nem is not None:
            self.nem.gen_for001(file)
        if self.ncv is not None:
            self.ncv.gen_for001(file)
        if self.section is not None:
            self.section.gen_for001(file)

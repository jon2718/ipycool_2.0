from regularregioncontainer import *
import copy
from output import Output

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
        ICoolObject.check_command_params_init(self, Repeat.command_params, **kwargs)
        Container.__init__(self)

    def __setattr__(self, name, value):
        self.__icool_setattr__(name, value)

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
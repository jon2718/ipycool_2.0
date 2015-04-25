from regularregioncontainer import *


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
        'Comment',
        'Repeat',
        ]

    command_params = {

    }

    def __init__(self, **kwargs):
        ICoolObject.check_command_params_init(self, Section.command_params, **kwargs)
        Container.__init__(self)

    def __setattr__(self, name, value):
        self.__icool_setattr__(name, value)

    def __str__(self):
        return_str = 'SECTION\n'
        return_str += str(Container.__str__(self))
        return_str += 'END_SECTION\n'
        return return_str

    def __repr__(self):
        return 'Section\n'
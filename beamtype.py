# -*- coding: utf-8 -*-
from container import *
from distribution import *
from correlation import *


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
        ICoolObject.check_command_params_init(self, BeamType.command_params, **kwargs)
        Container.__init__(self)

    def __setattr__(self, name, value):
        self.__icool_setattr__(name, value)

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
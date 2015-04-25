# -*- coding: utf-8 -*-
from icoolnamelist import *


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
            'type': 'Float',
            'req': False,
            'default': 0.003},
        'dcutm': {
            'desc': 'Kinetic energy of muons and other heavy particles, above which delta '
            'rays are discretely simulated [GeV] ',
            'doc': '',
            'type': 'Float',
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
            'type': 'Float',
            'req': False,
            'default': 1.0},
        'facmms': {
            'desc': 'Factor to correct screening angle squared χA2 in Moliere multiple ',
            'doc': '',
            'type': 'Float',
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
            'type': 'Float',
            'req': False,
            'default': 201},
        'parbunsc': {
            'desc': 'Number of muons per bunch for space charge calculation ',
            'doc': '',
            'type': 'Float',
            'req': False,
            'default': 4E12},
        'pdelev4': {
            'desc': 'Momentum for DELEV=4 calculation',
            'doc': '',
            'type': 'Float',
            'req': False,
            'default': 0.200},
        'wanga': {
            'desc': 'Wang parameter A ',
            'doc': 'The Wang distribution is given by '
            'd2σ/dp dΩ = A pMAX x (1-x) exp{-BxC – DpT} where x = pL / pMAX',
            'type': 'Float',
            'req': False,
            'default': 90.1},
        'wangb': {
            'desc': 'Wang parameter B',
            'doc': '',
            'type': 'Float',
            'req': False,
            'default': 3.35},
        'wangc': {
            'desc': 'Wang parameter C',
            'doc': '',
            'type': 'Float',
            'req': False,
            'default': 1.22},
        'wangd': {
            'desc': 'Wang parameter D',
            'doc': '',
            'type': 'Float',
            'req': False,
            'default': 4.66},
        'wangpmx': {
            'desc': 'Wang parameter pMAX (1.500) The sign of this quantity is used to select '
            'π+ or π- production.',
            'doc': '',
            'type': 'Float',
            'req': False,
            'default': 1.5},
        'wangfmx': {
            'desc': 'The maximum value of the Wang differential cross section',
            'doc': '',
            'type': 'Float',
            'req': False,
            'default': 13.706},
    }

    def __init__(self, **kwargs):
        ICoolObject.check_command_params_init(self, Ints.command_params, **kwargs)

    def __call__(self, **kwargs):
        pass
    
    def __setattr__(self, name, value):
        self.__icool_setattr__(name, value, Ints.command_params)

    def __str__(self):
        return ICoolObject.__str__(self, 'INTS')

    def __repr__(self):
        return '[Control variables: ]'

    def gen(self, file):
        ICoolObject.gen(self, file)

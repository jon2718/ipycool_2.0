# -*- coding: utf-8 -*-
from modeledcommandparameter import *


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
        if ModeledCommandParameter.check_command_params_init(self, Correlation.models, **kwargs) is False:
            sys.exit(0)

    def __call__(self, **kwargs):
        pass

    def __setattr__(self, name, value):
        self.__modeled_command_parameter_setattr__(name, value, Correlation.models)

    def __str__(self):
        return self.corrtyp + ':' + 'Correlation:' + \
            ModeledCommandParameter.__str__(self)
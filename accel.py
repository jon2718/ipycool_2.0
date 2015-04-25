# -*- coding: utf-8 -*-
from field import *


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
        if ModeledCommandParameter.check_command_params_init(self, Accel.models, **kwargs) is False:
            sys.exit(0)

    def __call__(self, **kwargs):
        pass

    def __setattr__(self, name, value):
        self.__modeled_command_parameter_setattr__(name, value, Accel.models)

    def __str__(self):
        return Field.__str__(self)

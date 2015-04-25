from icoolnamelist import *


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
        ICoolObject.check_command_params_init(self, Cont.command_params, **kwargs)

    def __call__(self, **kwargs):
        pass
    
    def __setattr__(self, name, value):
        self.__icool_setattr__(name, value, Cont.command_params)

    def __str__(self):
        return ICoolObject.__str__(self, 'CONT')

    def __repr__(self):
        return 'Requested repr for Cont'

    def gen(self, file):
        ICoolObject.gen(self, file)
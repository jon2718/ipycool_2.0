from drift import *
from hard_edge_transport import *
from hard_edge_sol import *
from accel import *
import sys


class Stage(HardEdgeTransport):
    """
    A final cooling stage comprises:
    HardEdgeTransport with transport field comprising:
    	(1) Drift (d1)
    	(2) HardEdgeSol
    	(3) Drift (d2)
    	(4) Accel (Model 1 for now)
    	(5) Drift (d3)
    """
  
    num_params = 3

    command_params_ext = {
        'd1_len': {'desc': 'Length of drift 1',
                 'doc': 'Initial drift region of stage length from entrance of stage to HardEdgeSol',
                 'type': 'FLoat',
                 'req': True,
                 'pos': None},
        'd2_len': {'desc': 'Length of drift 2',
                 'doc': 'Drift region between HardEdgeSol and Accel',
                 'type': 'FLoat',
                 'req': True,
                 'pos': None},

        'd3_len': {'desc': 'Length of drift 3',
                 'doc': 'Drift region between Accel and exit of stage',
                 'type': 'FLoat',
                 'req': True,
                 'pos': None},

        'transport_field':   {'desc': 'Transport field strength (Tesla)',
                 'doc': '',
                 'type': 'Float',
                 'req': True,
                 'pos': None},

        'absorber_field':   {'desc': 'Field strength (Tesla)',
                 'doc': '',
                 'type': 'Float',
                 'req': True,
                 'pos': None},

        'absorber_length': {'desc': 'Length of absorber region',
                 'doc': '',
                 'type': 'Float',
                 'req': True,
                 'pos': None},

        'rf_length': {'desc': 'Length of rf region',
                 'doc': '',
                 'type': 'Float',
                 'req': True,
                 'pos': None},

        'zstep': {'desc': 'Z step',
                  'doc': '',
                  'type': 'Float',
                  'req': True,
                  'pos': None},

        'outstep': {'desc': 'Output stepping (Meter)',
                    'doc': 'Increment for output steps for constant B Field region',
                    'type': 'Float',
                    'req': True,
                    'pos': None},

        'rhigh': {'desc': 'R high',
                  'doc': '',
                  'type': 'Float',
                  'req': True,
                  'pos': None},


        'hard_edge_sol': {'desc': 'Output stepping (Meter)',
                    'doc': 'Increment for output steps for constant B Field region',
                    'type': 'HardEdgeSol',
                    'req': False,
                    'pos': None},



        'drift1': {'desc': 'Output stepping (Meter)',
                    'doc': 'Increment for output steps for constant B Field region',
                    'type': 'Drift',
                    'req': False,
                    'pos': None},

        'drift2': {'desc': 'Output stepping (Meter)',
                    'doc': 'Increment for output steps for constant B Field region',
                    'type': 'Drift',
                    'req': False,
                    'pos': None},

        'drift3': {'desc': 'Output stepping (Meter)',
                    'doc': 'Increment for output steps for constant B Field region',
                    'type': 'Drift',
                    'req': False,
                    'pos': None},

        'freq': {'desc': 'Frequency in MHz',
                    'doc': 'Increment for output steps for constant B Field region',
                    'type': 'Float',
                    'req': True,
                    'pos': None},


        'grad': {'desc': 'Gradient on-axis at center of gap [MV/m]',
                    'doc': 'Increment for output steps for constant B Field region',
                    'type': 'Float',
                    'req': True,
                    'pos': None},

        'phase': {'desc': 'Phase shift [deg] {0-360}.',
                    'doc': 'Increment for output steps for constant B Field region',
                    'type': 'Float',
                    'req': True,
                    'pos': None},


        'rect_cyn': {'desc': 'Phase shift [deg] {0-360}.',
                    'doc': 'Increment for output steps for constant B Field region',
                    'type': 'Float',
                    'req': True,
                    'pos': None},


        'mode': {'desc': 'Phase shift [deg] {0-360}.',
                    'doc': 'Increment for output steps for constant B Field region',
                    'type': 'Float',
                    'req': True,
                    'pos': None}}
    
    def __init__(self, **kwargs):
        if ICoolObject.check_command_params_init(self, Stage.command_params_ext, **kwargs) is False:
            sys.exit(0)
        HardEdgeTransport.__init__(self, flip=False, bs=self.transport_field)
        
        drift1=Drift(slen=self.d1_len, zstep=self.zstep, rhigh=self.rhigh, outstep=self.outstep)
        drift2=Drift(slen=self.d2_len, zstep=self.zstep, rhigh=self.rhigh, outstep=self.outstep)
        drift3=Drift(slen=self.d3_len, zstep=self.zstep, rhigh=self.rhigh, outstep=self.outstep)
        rf=Accel(model='ez', freq=self.freq, phase=self.phase, grad=self.grad, rect_cyn=self.rect_cyn, mode=self.mode)
        hard_edge_sol=HardEdgeSol(slen=self.absorber_length, outstep=self.outstep, mtag='LH', geom='CBLOCK', zstep=self.zstep, bs=self.absorber_field,  rhigh=self.rhigh)

        self.add_enclosed_command(drift1)
        self.add_enclosed_command(hard_edge_sol)
        self.add_enclosed_command(drift2)
        rf_region = SRegion(slen=self.rf_length, nrreg=1, zstep=self.zstep)
        material = Material(mtag='VAC', geom='CBLOCK')
        rf_subregion = SubRegion(irreg=1, rlow=0, rhigh=self.rhigh, field=rf, material=material)
        rf_region.add_enclosed_command(rf_subregion)
        self.add_enclosed_command(rf_region)
        self.add_enclosed_command(drift3)

    def __call__(self, **kwargs):
        pass

    def __setattr__(self, name, value):
        self.__icool_setattr__(name, value)

    def __str__(self):
        return 'Stage'

    def gen_for001(self, file):
        HardEdgeTransport.gen_for001(self, file)

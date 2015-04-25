from sol import Sol
from material import Material
from subregion import SubRegion
from sregion import SRegion
from icoolobject import ICoolObject
from repeat import Repeat
from modeledcommandparameter import *


class HardEdgeSol(SRegion):
    """
    Hard edge solenoid comprises:
    (1) Entrance focusing region;
    (2) Non-focusing constant solenoid region;
    (3) Exit focusing region
    Lengths of each SRegion will be 1/3 total length specified.
    """
    begtag = ''
    endtag = ''
    num_params = 10

    command_params = {
        'mtag': {'desc': 'Material tag',
                 'doc': '',
                 'type': 'String',
                 'req': True,
                 'pos': None},
        'geom': {'desc': 'Geometry',
                 'doc': '',
                 'type': 'String',
                 'req': True,
                 'pos': None},
        'bs':   {'desc': 'Field strength (Tesla)',
                 'doc': '',
                 'type': 'Float',
                 'req': True,
                 'pos': None},
        'slen': {'desc': 'SRegion length',
                 'doc': '',
                 'type': 'Float',
                 'req': True,
                 'pos': None},
        'zstep': {'desc': 'Z step',
                  'doc': '',
                  'type': 'Float',
                  'req': True,
                  'pos': None},
        'rhigh': {'desc': 'R high',
                  'doc': '',
                  'type': 'Float',
                  'req': True,
                  'pos': None},
        'outstep': {'desc': 'Output stepping (Meter)',
                    'doc': 'Increment for output steps for constant B Field region',
                    'type': 'Float',
                    'req': True,
                    'pos': None},

        'sreg_entrance': {'desc': 'Entrance SRegion',
                          'doc': '',
                          'type': 'SRegion',
                          'req': False,
                          'pos': None},
        'sreg_exit':     {'desc': 'Exit SRegion',
                          'doc': '',
                          'type': 'SRegion',
                          'req': False,
                          'pos': None},
        'sreg_body': {'desc': 'Body SRegion',
                              'doc': '',
                              'type': 'SRegion',
                              'req': False,
                              'pos': None},
        'rep_body':  {'desc': 'Wrapped output SRegion',
                              'doc': '',
                              'type': 'Repeat',
                              'req': False,
                              'pos': None}
    }
    
    def __init__(self, **kwargs):
        if ICoolObject.check_command_params_init(self, HardEdgeSol.command_params, **kwargs) is False:
            sys.exit(0)
        material = Material(geom=self.geom, mtag=self.mtag)
        length = (float(1)/float(3))*self.slen
        print "length is: ", length
        
        # Entrance SRegion
        sol_ent = Sol(model='edge', ent_def=0, ex_def=0, foc_flag=2, bs=self.bs)
        ent_subregion = SubRegion(material=material, rlow=0, rhigh=self.rhigh, irreg=1, field=sol_ent)
        self.sreg_entrance = SRegion(zstep=self.zstep, nrreg=1, slen=length)
        self.sreg_entrance.add_enclosed_command(ent_subregion)

        # Exit SRegion
        sol_exit = Sol(model='edge', ent_def=0, ex_def=0, foc_flag=1, bs=self.bs)
        exit_subregion = SubRegion(material=material, rlow=0, rhigh=self.rhigh, irreg=1, field=sol_exit)
        self.sreg_exit = SRegion(zstep=self.zstep, nrreg=1, slen=length)
        self.sreg_exit.add_enclosed_command(exit_subregion)

        # Body SRegion
        sol_body = Sol(model='edge', ent_def=0, ex_def=0, foc_flag=0, bs=self.bs)
        body_subregion = SubRegion(material=material, rlow=0, rhigh=self.rhigh, irreg=1, field=sol_body)
        self.sreg_body = SRegion(zstep=self.zstep, nrreg=1, slen=length)
        self.sreg_body.add_enclosed_command(body_subregion)
        self.rep_body = Repeat.wrapped_sreg(outstep=self.outstep, sreg=self.sreg_body)


    def __call__(self, **kwargs):
        pass

    def __setattr__(self, name, value):
        self.__icool_setattr__(name, value, HardEdgeSol.command_params)

    def __str__(self):
        return 'HardEdgeSol'

    def gen_for001(self, file):
        self.sreg_entrance.gen_for001(file)
        self.rep_body.gen_for001(file)
        self.sreg_exit.gen_for001(file)


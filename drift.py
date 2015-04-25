from material import Material
from subregion import SubRegion
from sregion import SRegion
from icool_composite import ICoolComposite
from icoolobject import ICoolObject
from nofield import NoField
from repeat import Repeat


class Drift(SRegion):
    """
    Drift region.
    By default will generate a vacuum drift region with cylindrical geometry.
    """
    begtag = ''
    endtag = ''
    num_params = 0

    command_params = {
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

        'rep_drift':  {'desc': 'Wrapped output SRegion',
                              'doc': '',
                              'type': 'Repeat',
                              'req': False,
                              'pos': None}
    }

    def __init__(self, **kwargs):
        if ICoolObject.check_command_params_init(self, Drift.command_params, **kwargs) is False:
            sys.exit(0)
        material = Material(geom='CBLOCK', mtag='VAC')
        nf = NoField()
        sr = SubRegion(material=material, rlow=0, rhigh=self.rhigh, irreg=1, field=nf)
        sreg = SRegion(zstep=self.zstep, nrreg=1, slen=self.slen)
        sreg.add_enclosed_command(sr)
        self.rep_drift = Repeat.wrapped_sreg(outstep=self.outstep, sreg=sreg)

    def __call__(self, **kwargs):
        ICoolObject.__call__(self, kwargs)

    def __setattr__(self, name, value):
        self.__icool_setattr__(name, value, Drift.command_params)

    def __str__(self):
        return 'Drift'

    def gen_for001(self, file):
        self.rep_drift.gen_for001(file)
       

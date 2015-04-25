from namelists import *
from regions import *
from icoolobject import ICoolObject
from title import Title
from fields import *
from material import *


class ICoolInput(ICoolObject):

    """This is the actual generated ICoolInput from command objects
    Command objects include:
    Title, Cont, Bmt, Ints, Nhs, Nsc, Nzh, Nrh, Nem, Ncv and region command objects.
    Region command objects are the superclass of all region command objects and are
    subclassed into RegularRegion and PsuedoRegion command objects.

    RegularRegion command objects include: Section, Repeat, Cell and SRegion.
    Section, Begs, Repeat and Cell will typically contain other allowed region command objects
    such as SRegions as permitted by ICool.

    PseudoRegion command objects include:
        Aperture, Cutv, Denp, Dens, Disp, Dummy, Dvar, Edge, Grid, Output, Refp, Ref2, Reset, Rkick,
        Rotate, Taper, Tilt, Transport, Background, Bfield, ! and &

    title is a problem title object.
    cont is a control variables object.
    bmt is a beam generation variables object.
    ints is a physics interactions control variables object.
    nhs is a histogram defintion variables object.
    nsc is a scatterplot definition variables object.
    nzh is a z-history defintion variables object.
    nrh is a r-history defintion variables object.
    nem is an emittance plane definition variables object.
    ncv is a covariance plane definition variables object.
    sec is a region definition variables object, which contains all region definitions.
    """

    command_params = {
        'title': {'desc': 'Title of ICOOL simulation ',
                  'doc': '',
                  'type': 'Title',
                  'req': True,
                  'default': None},

        'cont': {'desc': 'ICOOL control variables ',
                 'doc': '',
                 'type': 'Cont',
                 'req': True,
                 'default': None},

        'bmt': {'desc': 'ICOOL beam generation variables ',
                'doc': '',
                'type': 'Bmt',
                'req': True,
                'default': None},

        'ints': {'desc': 'ICOOL interaction control variables ',
                 'doc': '',
                 'type': 'Ints',
                 'req': True,
                 'default': None},

        'nhs': {'desc': 'ICOOL histogram definition variables ',
                'doc': '',
                'type': 'Nhs',
                'req': False,
                'default': Nhs()},

        'nsc': {'desc': 'ICOOL scatterplot defintion variables ',
                'doc': '',
                'type': 'Nsc',
                'req': False,
                'default': Nsc()},

        'nzh': {'desc': 'ICOOL z history definition variables ',
                'doc': '',
                'type': 'Nzh',
                'req': False,
                'default': Nzh()},

        'nrh': {'desc': 'ICOOL r history definition variables ',
                'doc': '',
                'type': 'Nrh',
                'req': False,
                'default': Nrh()},

        'nem': {'desc': 'ICOOL emittance plane definition variables ',
                'doc': '',
                'type': 'Nem',
                'req': False,
                'default': Nem()},

        'ncv': {'desc': 'ICOOL covariance plane definition variables',
                'doc': '',
                'type': 'Ncv',
                'req': False,
                'default': Ncv()},

        'section': {'desc': 'ICOOL cooling section region definition ',
                    'doc': '',
                    'type': 'Section',
                    'req': True,
                    'default': None}}

    def __init__(self, **kwargs):
        ICoolObject.check_command_params_init(self, ICoolInput.command_params, **kwargs)
        ICoolObject.setdefault(self, ICoolInput.command_params, **kwargs)

    def __call__(self, kwargs):
        pass

    def __str__(self):
        return ICoolObject.__str__(self, 'CONT')

    def add_title(self, title):
        self.title = title

    def add_cont(self, cont):
        self.cont = cont

    def add_sec(self, sec):
        self.sec = sec

    def gen(self, f):
        file = open(f, 'w')
        if self.title is not None:
            self.title.gen_for001(file)
        if self.cont is not None:
            self.cont.gen_for001(file)
        if self.bmt is not None:
            self.bmt.gen_for001(file)
        if self.ints is not None:
            self.ints.gen_for001(file)
        if self.nhs is not None:
            self.nhs.gen_for001(file)
        if self.nsc is not None:
            self.nsc.gen_for001(file)
        if self.nzh is not None:
            self.nzh.gen_for001(file)
        if self.nrh is not None:
            self.nrh.gen_for001(file)
        if self.nem is not None:
            self.nem.gen_for001(file)
        if self.ncv is not None:
            self.ncv.gen_for001(file)
        if self.section is not None:
            self.section.gen_for001(file)
        file.close()

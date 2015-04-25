from region import *


class PseudoRegion(Region):

    """
    PseudoRegion commands include: APERTURE, CUTV, DENP, DENS, DISP, DUMMY, DVAR, EDGE, GRID
    OUTPUT, REFP, REF2, RESET, RKICK, ROTATE, TAPER, TILT, TRANSPORT, BACKGROUND, BFIELD, ENDB, ! or &
    """

    def __init__(self, **kwargs):
        pass

    def __str__(self):
        return '[A PseudoRegion can be either a APERTURE, CUTV, DENP, DENS, DISP, DUMMY, DVAR, EDGE, GRID\
                OUTPUT, REFP, REF2, RESET, RKICK, ROTATE, TAPER, TILT, TRANSPORT, BACKGROUND, BFIELD, ENDB, ! or &]'

    def __repr__(self):
        return '[A PseudoRegion can be either a APERTURE, CUTV, DENP, DENS, DISP, DUMMY, DVAR, EDGE, GRID\
                OUTPUT, REFP, REF2, RESET, RKICK, ROTATE, TAPER, TILT, TRANSPORT, BACKGROUND, BFIELD, ENDB, ! or &]'
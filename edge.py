from pseudoregion import *


class Edge(PseudoRegion):

    """EDGE Fringe field and other kicks for hard-edged field models
    1) edge type (A4) {SOL, DIP, HDIP, DIP3, QUAD, SQUA, SEX, BSOL, FACE}

    2.1) model # (I) {1}
    2.2-5) p1, p2, p3,p4 (R) model-dependent parameters

    Edge type = SOL
    p1: BS [T]
    If the main solenoid field is B, use p1=-B for the entrance edge and p1=+B for the exit edge.

    Edge type = DIP
    p1: BY [T]

    Edge type = HDIP
    p1: BX [T]

    Edge type = DIP3
    p1: rotation angle [deg]
    p2: BY0 [T]
    p3: flag 1:in 2:out

    Edge type = QUAD
    p1: gradient [T/m]

    Edge type = SQUA
    p1: gradient [T/m]

    Edge type = SEX
    p1: b2 [T/m2] (cf. C. Wang & L. Teng, MC 207)

    Edge type = BSOL
    p1: BS [T]
    p2: BY [T]
    p3: 0 for entrance face, 1 for exit face

    Edge type = FACE
    This gives vertical focusing from rotated pole faces.
    p1: pole face angle [deg]
    p2: radius of curvature of reference particle [m]
    p3: if not 0 => correct kick by factor 1/(1+delta)
    p4: if not 0 ==> apply horizontal focus with strength = (-vertical strength)
    If a FACE command is used before and after a sector dipole (DIP), you can approximate a rectangular dipole field.
    The DIP, HDIP, QUAD, SQUA, SEX and BSOL edge types use Scott Berg's HRDEND routine to find the change in transverse
    position and transverse momentum due to the fringe field.
    """

    def __init__(
            self,
            edge_type,
            model,
            model_parameters_list,
            name=None,
            metadata=None):
        PseudoRegion.__init__(self, name, metadata)
        self.edge_type = edge_type
        self.model = model
        self.model_parameters = model_parameters

class Edge(Field):

    """
    EDGE
    1) edge type (A4) {SOL, DIP, HDIP,DIP3,QUAD,SQUA,SEX, BSOL,FACE}
    2.1) model # (I) {1}
    2.2-5) p1, p2, p3,p4 (R) model-dependent parameters
    Edge type = SOL
    p1: BS [T]
    If the main solenoid field is B, use p1=-B for the entrance edge and p1=+B for the exit edge.
    Edge type = DIP
    p1: BY [T]
    Edge type = HDIP
    p1: BX [T]
    Edge type = DIP3
    p1: rotation angle [deg]
    p2: BY0 [T]
    p3: flag 1:in 2:out
    Edge type = QUAD
    p1: gradient [T/m]
    Edge type = SQUA
    p1: gradient [T/m]
    Edge type = SEX
    p1: b2 [T/m2] (cf. C. Wang & L. Teng, MC 207)
    Edge type = BSOL
    p1: BS [T]
    p2: BY [T]
    p3: 0 for entrance face, 1 for exit face
    Edge type = FACE
    This gives vertical focusing from rotated pole faces.
    p1: pole face angle [deg]
    p2: radius of curvature of reference particle [m]
    p3: if not 0 => correct kick by the factor 1 / (1+δ)
    p4: if not 0 => apply horizontal focus with strength = (-vertical strength)
    If a FACE command is used before and after a sector dipole ( DIP ), you can approximate a rectangular dipole field.
    The DIP, HDIP, QUAD, SQUA, SEX and BSOL edge types use Scott Berg’s HRDEND routine to find the change in
    transverse position and transverse momentum due to the fringe field.
    """

    begtag = 'EDGE'
    endtag = ''

    models = {
        'model_descriptor': {
            'desc': 'Name of model parameter descriptor',
            'name': 'model',
            'num_parms': 6,
            'for001_format': {
                'line_splits': [
                    1,
                    5]}},
        'sol': {
            'desc': 'Solenoid',
                    'doc': '',
                    'icool_model_name': 'SOL',
                    'parms': {
                        'model': {
                            'pos': 1,
                            'type': 'String',
                            'doc': ''},
                        'bs': {
                            'pos': 3,
                            'type': 'Real',
                            'doc': 'p1: BS [T] '
                            'If the main solenoid field is B, use p1=-B for the entrance edge and p1=+B for the '
                            'exit edge. (You can use this to get a tapered field profile)'}}},
    }

    def __init__(self, **kwargs):
        Field.__init__(self, 'EDGE', kwargs)

    def __call__(self, **kwargs):
        Field.__call__(self, kwargs)

    def __setattr__(self, name, value):
        if name == 'ftag':
            if value == 'EDGE':
                object.__setattr__(self, name, value)
            else:
                # Should raise exception here
                print '\n Illegal attempt to set incorrect ftag.\n'
        else:
            Field.__setattr__(self, name, value)

    def __str__(self):
        return Field.__str__(self)

    def gen_fparm(self):
        Field.gen_fparm(self)
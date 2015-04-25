# -*- coding: utf-8 -*-
# from modeledcommandparameter import *
from modeledcommandparameter import ModeledCommandParameter


class Material(ModeledCommandParameter):

    """
    A Material is a:
    (1) MTAG (A) material composition tag
    (2) MGEOM (A) material geometry tag
    (3-12) GPARM (R) 10 parameters that describe the geometry of the material

    Enter MTAG in upper case.
    Valid MTAG'S are:

    VAC vacuum (i.e., no material)
    GH gaseous hydrogen
    GHE gaseous helium
    LH liquid hydrogen
    LHE liquid helium
    LI BE B C AL TI FE CU W HG PB (elements)
    LIH lithium hydride
    CH2 polyethylene
    SS stainless steel (alloy 304)

    Valid MGEOM's are:

    NONE use for vacuum
    10*0.

    CBLOCK cylindrical block
    10*0.
    ...

    """
    begtag = ''
    endtag = ''
    
    materials = {
        'VAC': {'desc': 'Vacuum (no material)', 'icool_material_name': ''},
        'GH': {'desc': 'Gaseous hydrogen'},
        'GHE': {'desc': 'Gaseous helium'},
        'LH': {'desc': 'Liquid hydrogen'},
        'LHE': {'desc': 'Liquid helium'},
        'LI': {'desc': 'Lithium'},
        'BE': {'desc': 'Berylliyum'},
        'B': {'desc': 'Boron'},
        'C': {'desc': 'Carbon'},
        'AL': {'desc': 'Aluminum'},
        'TI': {'desc': 'Titanium'},
        'FE': {'desc': 'Iron'},
        'CU': {'desc': 'Copper'},
        'W': {'desc': 'Tungsten'},
        'HG': {'desc:': 'Mercury'},
        'PB': {'desc:': 'Lead'}
    }

    models = {
        'model_descriptor': {
            'desc': 'Geometry',
            'name': 'geom',
            'num_parms': 12,
            'for001_format': {
                'line_splits': [1, 1, 10]}},
        'VAC': {
            'desc': 'Vacuum',
            'doc': 'Vacuum region.  Specify vacuum for mtag.  Geom will be set to NONE.',
            'parms': {
                'mtag': {
                           'pos': 1, 'type': 'String', 'doc': ''}}},
        'CBLOCK': {
            'desc': 'Cylindrical block',
            'doc': 'Cylindrical block',
            'parms': {
                'mtag': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'geom': {
                    'pos': 2, 'type': 'String', 'doc': ''}}},
        'ASPW': {
            'desc': 'Azimuthally Symmetric Polynomial Wedge absorber region', 'doc': 'Edge shape given by '
                    'r(dz) = a0 + a1*dz + a2*dz^2 + a3*dz^3 in the 1st quadrant and '
                    'where dz is measured from the wedge center. '
                    '1 z position of wedge center in region [m] '
                    '2 z offset from wedge center to edge of absorber [m] '
                    '3 a0 [m] '
                    '4 a1 '
                    '5 a2 [m^(-1)] '
                    '6 a3 [m^(-2)]',
            'parms': {
                'mtag': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'geom': {
                    'pos': 2, 'type': 'String', 'doc': ''},
                'zpos': {
                    'pos': 3, 'type': 'Real', 'doc': ''},
                'zoff': {
                    'pos': 4, 'type': 'Real', 'doc': ''},
                'a0': {
                    'pos': 5, 'type': 'Real', 'doc': ''},
                'a1': {
                    'pos': 6, 'type': 'Real', 'doc': ''},
                'a2': {
                    'pos': 7, 'type': 'Real', 'doc': ''},
                'a3': {
                    'pos': 8, 'type': 'Real', 'doc': ''}}},
        'ASRW': {
            'desc': 'Azimuthally Symmetric Polynomial Wedge absorber region',
            'doc':  'Edge shape given by '
                    'r(dz) = a0 + a1*dz + a2*dz^2 + a3*dz^3 in the 1st quadrant and '
                    'where dz is measured from the wedge center. '
                    '1 z position of wedge center in region [m] '
                    '2 z offset from wedge center to edge of absorber [m] '
                    '3 a0 [m] '
                    '4 a1 '
                    '5 a2 [m^(-1)] '
                    '6 a3 [m^(-2)]',
            'parms': {
                'mtag': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'geom': {
                    'pos': 2, 'type': 'String', 'doc': ''},
                'zpos': {
                    'pos': 3, 'type': 'Real', 'doc': ''},
                'zoff': {
                    'pos': 4, 'type': 'Real', 'doc': ''},
                'a0': {
                    'pos': 5, 'type': 'Real', 'doc': ''},
                'a1': {
                    'pos': 6, 'type': 'Real', 'doc': ''},
                'a2': {
                    'pos': 7, 'type': 'Real', 'doc': ''},
                'a3': {
                    'pos': 8, 'type': 'Real', 'doc': ''}}},
        'HWIN': {
            'desc': 'Hemispherical absorber end region',
            'doc': '1 end flag {-1: entrance, +1: exit} '
                   '2 inner radius of window[m] '
                   '3 window thickness [m] '
                   '4 axial offset of center of spherical window from start of end region [m]',
            'parms': {
                'mtag': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'geom': {
                    'pos': 2, 'type': 'String', 'doc': ''},
                'end_flag': {
                    'pos': 3, 'type': 'Real', 'doc': '1 end flag {-1: entrance, +1: exit} '},
                'in_rad': {
                    'pos': 4, 'type': 'Real', 'doc': 'Inner radius of window'},
                'thick': {
                    'pos': 5, 'type': 'Real', 'doc': 'Thickness of window'},
                'offset': {
                    'pos': 6, 'type': 'Real', 'doc': 'Axial offset of center of spherical '
                                                     'window from start of end region [m]'}}},
        'NIA': {
            'desc': 'Non-isosceles absorber',
            'doc': '1 zV distance of wedge “center” from start of region [m] '
                   '2 z0 distance from center to left edge [m] '
                   '3 z1 distance from center to right edge [m] '
                   '4 θ0 polar angle from vertex of left edge [deg] '
                   '5 φ0 azimuthal angle of left face [deg] '
                   '6 θ1 polar angle from vertex of right edge [deg] '
                   '7 φ1 azimuthal angle of right face [deg]',
            'parms': {
                'mtag': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'geom': {
                    'pos': 2, 'type': 'String', 'doc': ''},
                'zv': {
                    'pos': 3, 'type': 'Real', 'doc': 'Distance of wedge “center” from start of region [m]'},
                'z0': {
                    'pos': 4, 'type': 'Real', 'doc': 'Distance from center to left edge [m] '},
                'z1': {
                    'pos': 5, 'type': 'Real', 'doc': 'Distance from center to right edge [m]}'},
                'θ0': {
                    'pos': 6, 'type': 'Real', 'doc': 'Polar angle from vertex of left edge [deg]'},
                'φ0': {
                    'pos': 7, 'type': 'Real', 'doc': 'Azimuthal angle of left face [deg]'},
                'θ1': {
                    'pos': 8, 'type': 'Real', 'doc': 'Polar angle from vertex of right edge [deg] '},
                'φ1': {
                    'pos': 9, 'type': 'Real', 'doc': 'Azimuthal angle of right face [deg]'}}},
        'PWEDGE': {
            'desc': 'Asymmetric polynomial wedge absorber region',
            'doc': 'Imagine the wedge lying with its narrow end along the x axis. The wedge is symmetric about the '
                   'x-y plane. The edge shape is given by dz(x) = a0 + a1*x + a2*x^2 + a3*x^3 '
                   'where dz is measured from the x axis.',
            'parms': {
                'mtag': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'geom': {
                    'pos': 2, 'type': 'String', 'doc': ''},
                'init_vertex': {
                    'pos': 3, 'type': 'Real', 'doc': 'Initial position of the vertex along the x axis [m]'},
                'z_wedge_vertex': {
                    'pos': 4, 'type': 'Real', 'doc': 'z position of wedge vertex [m] '},
                'az': {
                    'pos': 5, 'type': 'Real', 'doc': 'Azimuthal angle of vector pointing to vertex in plane of wedge w.r.t. +ve x-axis [deg]'},
                'width': {
                    'pos': 6, 'type': 'Real', 'doc': 'Total width of wedge in dispersion direction [m]'},
                'height': {
                    'pos': 7, 'type': 'Real', 'doc': 'Total height of wedge in non-dispersion direction [m]'},
                'a0': {
                    'pos': 8, 'type': 'Real', 'doc': 'Polar angle from vertex of right edge [deg] '},
                'a1': {
                    'pos': 9, 'type': 'Real', 'doc': 'Azimuthal angle of right face [deg]'},
                'a2': {
                    'pos': 10, 'type': 'Real', 'doc': 'Polar angle from vertex of right edge [deg] '},
                'a3': {
                    'pos': 11, 'type': 'Real', 'doc': 'Azimuthal angle of right face [deg]'}}},
        'RING': {
            'desc': 'Annular ring of material',
            'doc': 'This is functionally equivalent to defining a region with two radial subregions, the first of '
                   'which has vacuum as the material type. However, the boundary crossing algorithm used for RING is '
                   'more sophisticated and should give more accurate simulations.',
            'parms': {
                'mtag': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'geom': {
                    'pos': 2, 'type': 'String', 'doc': ''},
                'inner': {
                    'pos': 3, 'type': 'Real', 'doc': 'Inner radius (R) [m]'},
                'outer': {
                    'pos': 4, 'type': 'Real', 'doc': 'Outer radius (R) [m]'}}},
        'WEDGE': {
            'desc': 'Asymmetric wedge absorber region',
            'doc': 'We begin with an isosceles triangle, sitting on its base, vertex at the top. '
                   'The base-to-vertex distance is W. The full opening angle at the vertex is A. Using '
                   'two of these triangles as sides, we construct a prism-shaped wedge. The distance from '
                   'one triangular side to the other is H. The shape and size of the wedge are now established. '
                   'We define the vertex line of the wedge to be the line connecting the vertices of its two '
                   'triangular sides.  Next, we place the wedge in the right-handed ICOOL coordinate system. '
                   'The beam travels in the +Z direction. Looking downstream along the beamline (+Z into the page), '
                   '+X is horizontal and to the left, and +Y is up.  Assume the initial position of the wedge is as '
                   'follows: The vertex line of the wedge is vertical and lies along the Y axis, extending from Y = -H/2 '
                   'to Y = +H/2. The wedge extends to the right in the direction of -X, such that it is symmetric about '
                   "the XY plane. (Note that it is also symmetric about the XZ plane.) From the beam's point of view, "
                   'particles passing on the +X side of the Y axis will not encounter the wedge, while particles passing '
                   'on the -X side of the Y axis see a rectangle of height H and width W, centered in the Y direction, with '
                   'Z thickness proportional to -X.  '
                   'By setting parameter U to a non-zero value, the user may specify that the wedge is to be '
                   'translated in the X direction. If U>0, the wedge is moved (without rotation) in the +X direction. '
                   'For example, if U = W/2, then the wedge is centered in the X direction; its vertex is at X = W/2 '
                   'and its base is at X = -W/2. Note that the wedge is still symmetric about both the XY plane and '
                   'the XZ plane. '
                   'Next, the wedge may be rotated about the Z axis by angle PHI. Looking downstream in the beam '
                   'direction, positive rotations are clockwise and negative rotations are counter-clockwise. For '
                   'example, setting PHI to 90 degrees rotates the wedge about the Z axis so that its vertex line is '
                   'parallel to the X axis and on top, while its base is parallel to the XZ plane and at the bottom. In '
                   'general this rotation breaks the symmetry about the XZ plane, but the symmetry about the XY '
                   'plane is maintained. '
                   'Finally, the wedge is translated in the Z direction by a distance Zv, so that its XY symmetry plane '
                   'lies a distance Zv downstream of the start of the region. Usually Zv should be at least large '
                   'enough so that the entire volume of the wedge lies within its region, i.e. Zv .ge. W tan (A/2), the '
                   'maximum Z half-thickness of the wedge. As well, the region usually should be long enough to '
                   'contain the entire volume of the wedge, i.e. RegionLength .ge. Zv + W tan (A/2). Wedges that do '
                   'lie completely within their region retain their symmetry about the XY plane Z=Zv.  '
                   'If portions of a wedge lie outside their region in Z, then the volume of the wedge lying outside '
                   'the region is ignored when propagating particles through the wedge. Such a wedge will grow in '
                   'thickness until it reaches the region boundary, but will not extend beyond it. In such cases, '
                   'wedges may lose their symmetry about the XY plane Z=Zv.'
                   'Wedges may be defined such that they extend outside the radial boundaries of the radial '
                   'subregion within which they are defined. However, any portion of the wedge volume lying inside the inner '
                   'radial boundary or outside the outer radial boundary is ignored when propagating particles through '
                   'the wedge. For example, if the user intends that an entire radial subregion of circular cross-section be '
                   'filled with a wedge, then it is clear that the corners of the wedge must extend outside the radial region, '
                   "but particles passing outside the wedge's radial subregion will not see the wedge at all.  "
                   'In short, we may say that although it is permitted (and sometimes essential) to define a wedge to '
                   'be larger than its subregion, for the purposes of particle propagation the wedge is always trimmed at the '
                   "region's Z boundaries and the subregion's radial boundaries. Any volume within the region and subregion "
                   'that is not occupied by the material specified for the wedge is assumed to be vacuum.'
                   '------------------------------------------------------------------------------------------------------------'
                   'Example 1: Within a region 0.4 meters long in Z, within a radial subregion extending from the Z axis out '
                   'to a radius of 0.3 meters, a wedge is to fill the X<0 (right) half of the 0.3 meter aperture of the '
                   'subregion, and increase in Z thickness proportional to -X, such that it is 0.2 meters thick at the '
                   'rightmost point in the subregion (X=-0.3, Y=0).  The wedge is to be 0.2 meters thick at a point 0.3 '
                   'meters from its vertex. The half-thickness is 0.1 meters, the half-opening angle is '
                   'atan (0.1/0.3) = 18.4 degrees, so the full opening angle of the wedge A is 36.8 degrees. The width '
                   '(X extent) of the wedge must be 0.3 meters, and the height (Y extent) of the wedge must be 0.6 meters. '
                   'Two corners of the wedge extend well beyond the subregion, but they will be ignored during particle '
                   'propagation. The wedge does not need to be translated in X (U = 0) nor does it need to be rotated '
                   'about the Z axis (PHI = 0). For convenience we center the wedge (in Z) within its region, '
                   'so Zv = 0.2 meters. Since the maximum half-thickness of the wedge is only 0.1 meters, the wedge '
                   'does not extend beyond (or even up to) the Z boundaries of the region. The volume within the region '
                   'and subregion but outside the wedge is assumed to be vacuum.'
                   '------------------------------------------------------------------------------------------------------------'
                   'Example 2: In the same region and subregion, we need a wedge with the same opening angle, '
                   'but filling the entire aperture of the subregion, thickness gradient in the +Y direction, thickness = '
                   '0 at the lowest point in the subregion (X=0, Y=-0.3).'
                   'The wedge must now have H = W = 0.6 meters so it can fill the entire aperture of the subregion.'
                   'From its initial position, it must first be translated 0.3 meters in the +X direction (U = 0.3) to '
                   "center it in the subregion's aperture, and then (from the perspective of someone looking "
                   'downstream along the beam) rotated counterclockwise 90 degrees (PHI = -90.) so that the Z '
                   'thickness increases proportionally to +Y. Since the wedge has the same opening angle as before '
                   'but has twice the width, its maximum Z thickness is now 0.4 meters, just barely fitting between '
                   'the Z boundaries of the region if Zv = 0.2 meters. All four corners of the wedge now extend '
                   "outside the radial subregion's outer boundary, but they will be ignored during particle "
                   'propagation.” {S.B.}'
                   'The wedge geometry can accept a second MTAG parameter in the SREGION construct. The first material '
                   'refers to the interior of the wedge. The second material, if present, refers to the exterior of the wedge. '
                   'If a second MTAG parameter is not present, vacuum is assumed.',
            'parms': {
                'mtag': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'geom': {
                    'pos': 2, 'type': 'String', 'doc': ''},
                'vert_ang': {
                    'pos': 3, 'type': 'Real', 'doc': 'Full angle at vertex, α (or A) [degrees]the x axis [m]'},
                'vert_init': {
                    'pos': 4, 'type': 'Real', 'doc': 'Initial position of the vertex along the x axis, U [m]'},
                'vert_z': {
                    'pos': 5, 'type': 'Real', 'doc': 'Z position of wedge vertex, Zv [m]'},
                'vert_az': {
                    'pos': 6, 'type': 'Real', 'doc': 'azimuthal angle φ of vector pointing to vertex in plane of wedge w.r.t. +ve x-axis [deg]'},
                'width': {
                    'pos': 7, 'type': 'Real', 'doc': 'Total width of wedge in dispersion direction, w [m]'},
                'height': {
                    'pos': 8, 'type': 'Real', 'doc': 'Total height of wedge in non-dispersion direction, h [m]'}}}}

    def __init__(self, **kwargs):
        if ModeledCommandParameter.check_command_params_init(self, Material.models, **kwargs) is False:
            sys.exit(0)

    def __setattr__(self, name, value):
        self.__modeled_command_parameter_setattr__(name, value, Material.models)

    def __str__(self):
        return 'Material:' + ModeledCommandParameter.__str__(self)

    """def gen_mparm(self):
        self.mparm = [0] * 12
        cur_model = self.get_model_dict(self.geom)
        for key in cur_model:
            pos = int(cur_model[key]['pos']) - 1
            val = getattr(self, key)
            self.mparm[pos] = val
        print self.mparm

    def gen(self, file):
        file.write('\n')
        file.write(self.mtag)
        file.write('\n')
        file.write(self.mgeom)
        file.write('\n')
        for s in mparm:
            file.write(s)
            file.write(" ")"""
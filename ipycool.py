# -*- coding: utf-8 -*-

from icoolinput import *

"""Nomenclature:

An ICOOL input file consists of:
1. Problem title
2. General control variables
3. Beam generation variables
4. Physics interactions control variables
5. Histogram definition variables
6. Scatterplot definition variables
7. Z-history definition variables
8. R-history definition variables
9. Emittance plane definition variables
10. Covariance plane definition variables
11. Region definition variables.
** Note that region definition variables are referred to in the ICOOL Manual and
herein as commands.

This program will use of following object definitions:
Namelists.  Namelists in the for001.dat file are preceded by an '&'
sign (e.g., &cont).

Namelists include:
CONT: Control Variables
BMT: Beam Generation Variables
INTS: Phyiscs Interactions Control Variables
NHS: Histogram Definition Variables
NSC: Scatterplot definition Variables
NZH: Z-History Definition Variables
NRH: R-History Definition Variables
NEM: Emittance Plane Definition Variables
NCV: Covariance Plane Definition Variables


Namelist variables:
Each of the above namelists is associated with a respective set of variables.

Commands:
Commands comprise both Regular Region Commands and Pseudoregion Commands

Regular Region Commands:
SECTION
BEGS
REPEAT
CELL
SREGION
ENDREPEAT
ENDCELL
ENDSECTION

Psuedoregion Commands:
APERTURE
CUTV
DENP
DENS
DISP
DUMMY
DVAR
EDGE
GRID
OUTPUT
RESET
RKICK
ROTATE
TAPER
TILT
TRANSPORT
BACKGROUND
BFIELD
ENDB
!
&

Command parameters:
Each regular and pseduoregion command is respectively associated with a set of command parameters.
"""
from IPython.core.magic_arguments import (argument, magic_arguments,
                                          parse_argstring)
from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)

#@register_line_magic


@magic_arguments()
@argument('-o', '--option', help='An optional argument.')
@argument('arg', type=int, help='An integer positional argument.')
def ipycool(self, arg):
    """ A really cool ipycool magic command.

    """
    args = parse_argstring(ipycool, arg)


@magic_arguments()
@register_line_magic
def icool():
    "ICOOL"
    exec('!icool')
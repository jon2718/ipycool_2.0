from pseudoregion import *


class Output(PseudoRegion):
    begtag = 'OUTPUT'
    endtag = ''

    num_params = 0
    for001_format = {'line_splits': [0]}

    command_params = {}

    def __init__(self):
        pass
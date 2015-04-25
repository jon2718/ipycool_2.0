from regularregion import *


class Begs(RegularRegion):

    def __init__(self):
        RegularRegion.__init(self, None, None)

    def gen(self, file):
        file.write('\n')
        file.write('BEGS')
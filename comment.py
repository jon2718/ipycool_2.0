from pseudoregion import *


class Comment(PseudoRegion):

    def __init__(self, comment):
        PseudoRegion.__init__(self, None)
        self.comment = comment

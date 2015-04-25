from icoolnamelist import *
from container import *


class ICoolNameListContainer(ICoolNameList, Container):

    def gen_for001(self, file):
        ICoolNameList.gen_for001(self, file)
        Container.gen_for001(self, file)
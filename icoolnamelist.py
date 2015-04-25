from icoolobject import *


class ICoolNameList(ICoolObject):

    def gen_for001(self, file):
        name = self.__class__.__name__.lower()
        file.write('&')
        file.write(name)
        file.write(' ')
        count = 0
        items_per_line = 5
        for key in self.command_params:
            if hasattr(self, key):
                file.write(str(key))
                file.write('=')
                file.write(self.for001_str_gen(getattr(self, key)))
                file.write(' ')
                count = count + 1
                if count % items_per_line == 0:
                    file.write('\n')
        file.write('/')
        file.write('\n')

        
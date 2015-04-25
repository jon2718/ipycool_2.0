from icoolobject import *


class Region(ICoolObject):

    def __init__(self, kwargs):
        pass

    def __call__(self, **kwargs):
        pass

    def __str__(self):
        return '[A Region can be either a RegularRegion or PseudoRegion.]'

    def __repr__(self):
        return '[A Region can be either a RegularRegion or PseudoRegion.]'

    def __setattr__(self, name, value):
        return

    def gen_for001(self, file):
        if hasattr(self, 'begtag'):
            file.write(self.get_begtag())
            file.write('\n')
        parm = self.gen_parm()
        splits = self.get_line_splits()
        count = 0
        split_num = 0
        cur_split = splits[split_num]
        for command in parm:
            if count == cur_split:
                file.write('\n')
                count = 0
                split_num = split_num + 1
                cur_split = splits[split_num]
            if hasattr(command, 'gen_for001'):
                command.gen_for001(file)
            else:
                file.write(self.for001_str_gen(command))
            file.write(' ')
            count = count + 1
        file.write('\n')
from icoolobject import ICoolObject

class Title(ICoolObject):
    command_params = {
        'title': {'desc': 'Title of ICOOL simulation',
                  'doc': '',
                  'type': 'String',
                  'req': True,
                  'default': None}

    }

    def __init__(self, **kwargs):
      if ICoolObject.check_command_params_init(self, Title.command_params, **kwargs) is False:
          sys.exit(0)

    def __str__(self):
        return 'Problem Title: ' + self.title + '\n'

    def __repr__(self):
        return 'Problem Title: ' + self.title + '\n'

    def __setattr__(self, name, value):
        self.__icool_setattr__(name, value, Title.command_params)

    def gen_for001(self, file):
        file.write(self.title)
        file.write('\n')